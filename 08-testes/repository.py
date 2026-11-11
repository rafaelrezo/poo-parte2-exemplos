import csv
import io
import math
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(frozen=True)
class Aquisicao:
    sessao: str
    ciclo: int
    nivel: float

    def __post_init__(self):
        if not isinstance(self.sessao, str) or not self.sessao.strip():
            raise ValueError("sessao invalida")
        if type(self.ciclo) is not int or self.ciclo <= 0:
            raise ValueError("ciclo invalido")
        if (type(self.nivel) not in (int, float) or not 0 <= self.nivel <= 100
                or not math.isfinite(self.nivel)):
            raise ValueError("nivel invalido")


class HistoricoSQLite:
    def __init__(self, conexao):
        self._conexao = conexao
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS aquisicoes (
                    sessao TEXT NOT NULL,
                    ciclo INTEGER NOT NULL CHECK (ciclo > 0),
                    nivel REAL NOT NULL CHECK (nivel BETWEEN 0 AND 100),
                    PRIMARY KEY (sessao, ciclo)
                )
            """)

    def salvar(self, aquisicao):
        with self._conexao:
            cursor = self._conexao.execute("""
                INSERT INTO aquisicoes (sessao, ciclo, nivel) VALUES (?, ?, ?)
                ON CONFLICT (sessao, ciclo) DO NOTHING
            """, (aquisicao.sessao, aquisicao.ciclo, aquisicao.nivel))
            if cursor.rowcount == 0:
                atual = self._conexao.execute("""
                    SELECT nivel FROM aquisicoes WHERE sessao = ? AND ciclo = ?
                """, (aquisicao.sessao, aquisicao.ciclo)).fetchone()
                if atual[0] != aquisicao.nivel:
                    raise ValueError("identidade com conteudo diferente")
                return False
            return True

    def listar(self):
        linhas = self._conexao.execute("""
            SELECT sessao, ciclo, nivel FROM aquisicoes ORDER BY sessao, ciclo
        """).fetchall()
        return [Aquisicao(*linha) for linha in linhas]


def exportar_csv(aquisicoes):
    saida = io.StringIO(newline="")
    escritor = csv.writer(saida, lineterminator="\n")
    escritor.writerow(["sessao", "ciclo", "nivel"])
    for aquisicao in aquisicoes:
        escritor.writerow([aquisicao.sessao, aquisicao.ciclo, aquisicao.nivel])
    return saida.getvalue()


def main():
    with TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "historico.db"
        with closing(sqlite3.connect(caminho)) as conexao:
            historico = HistoricoSQLite(conexao)
            historico.salvar(Aquisicao("ensaio", 1, 48.5))
            historico.salvar(Aquisicao("ensaio", 1, 48.5))
            historico.salvar(Aquisicao("ensaio", 2, 49.0))
        with closing(sqlite3.connect(caminho)) as conexao:
            itens = HistoricoSQLite(conexao).listar()
            assert len(itens) == 2
            print(exportar_csv(itens), end="")


if __name__ == "__main__":
    main()
