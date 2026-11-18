from planta.modelo import Aquisicao


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
