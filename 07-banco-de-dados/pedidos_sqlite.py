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


def registrar(conexao, numero, item, setor, valor):
    with conexao:  # transação: confirma ao sair do bloco, desfaz se houver erro
        cursor = conexao.execute("""
            INSERT INTO pedidos (numero, item, setor, valor) VALUES (?, ?, ?, ?)
            ON CONFLICT (numero) DO NOTHING
        """, (numero, item, setor, valor))
    return cursor.rowcount == 1  # 1 linha inserida; 0 se o número já existia


def contar(conexao):
    return conexao.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


def buscar(conexao, numero):
    return conexao.execute(
        "SELECT numero, item, setor, valor FROM pedidos WHERE numero = ?", (numero,)
    ).fetchone()


def listar_do_setor(conexao, setor):
    return conexao.execute(
        "SELECT numero, item, valor FROM pedidos WHERE setor = ? ORDER BY numero", (setor,)
    ).fetchall()


def faturamento_por_setor(conexao):
    return conexao.execute("""
        SELECT setor, COUNT(*), SUM(valor) FROM pedidos
        GROUP BY setor ORDER BY setor
    """).fetchall()


def main():
    with closing(sqlite3.connect("lanchonete.db")) as conexao:
        criar_tabela(conexao)
        print(f"pedidos ao abrir o programa: {contar(conexao)}")

        for numero, item, setor, valor in [(1, "X-burguer", "cozinha", 18.0),
                                           (2, "suco de laranja", "bar", 7.5),
                                           (3, "misto quente", "cozinha", 12.0)]:
            if registrar(conexao, numero, item, setor, valor):
                print(f"  pedido {numero} registrado")
            else:
                print(f"  pedido {numero} ja existia, nada foi gravado")

        print(f"pedidos no banco: {contar(conexao)}")
        print(f"pedido 2: {buscar(conexao, 2)}")
        print(f"pedidos da cozinha: {listar_do_setor(conexao, 'cozinha')}")
        for setor, quantidade, total in faturamento_por_setor(conexao):
            print(f"  {setor}: {quantidade} pedido(s), R$ {total:.2f}")


if __name__ == "__main__":
    main()
