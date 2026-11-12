import sqlite3
from contextlib import closing


class Caixa:
    def __init__(self, conexao):
        self._conexao = conexao

    def vender(self, item, setor, valor):
        with self._conexao:
            ultimo = self._conexao.execute("SELECT MAX(numero) FROM pedidos").fetchone()[0]
            numero = (ultimo or 0) + 1
            self._conexao.execute(
                "INSERT INTO pedidos (numero, item, setor, valor) VALUES (?, ?, ?, ?)",
                (numero, item, setor, valor))
        print(f"caixa: pedido {numero} registrado")
        return numero


class Relatorio:
    def __init__(self, conexao):
        self._conexao = conexao

    def imprimir(self):
        linhas = self._conexao.execute("""
            SELECT setor, SUM(valor) FROM pedidos GROUP BY setor ORDER BY setor
        """).fetchall()
        print("faturamento por setor:")
        for setor, total in linhas:
            print(f"  {setor}: R$ {total:.2f}")


def criar_tabela(conexao):
    with conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                numero INTEGER PRIMARY KEY,
                item   TEXT    NOT NULL,
                setor  TEXT    NOT NULL,
                valor  REAL    NOT NULL CHECK (valor > 0)
            )
        """)


def main():
    with closing(sqlite3.connect(":memory:")) as conexao:
        criar_tabela(conexao)
        caixa = Caixa(conexao)
        caixa.vender("X-burguer", "cozinha", 18.0)
        caixa.vender("suco de laranja", "bar", 7.5)
        caixa.vender("misto quente", "cozinha", 12.0)
        Relatorio(conexao).imprimir()


if __name__ == "__main__":
    main()
