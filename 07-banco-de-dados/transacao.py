import sqlite3
from contextlib import closing


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


def registrar_lote(conexao, lote):
    """Grava todos os pedidos do lote ou nenhum."""
    with conexao:
        for pedido in lote:
            conexao.execute(
                "INSERT INTO pedidos (numero, item, setor, valor) VALUES (?, ?, ?, ?)", pedido)


def contar(conexao):
    return conexao.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


def main():
    with closing(sqlite3.connect(":memory:")) as conexao:  # banco só em memória, para a demonstração
        criar_tabela(conexao)

        registrar_lote(conexao, [(1, "X-burguer", "cozinha", 18.0),
                                 (2, "suco de laranja", "bar", 7.5)])
        print(f"depois do primeiro lote: {contar(conexao)} pedidos")

        try:
            registrar_lote(conexao, [(3, "misto quente", "cozinha", 12.0),
                                     (4, "agua", "bar", 0.0)])  # valor invalido
        except sqlite3.IntegrityError as erro:
            print(f"segundo lote recusado: {erro}")
        print(f"depois do segundo lote: {contar(conexao)} pedidos")


if __name__ == "__main__":
    main()
