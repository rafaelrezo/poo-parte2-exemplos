import sqlite3
from contextlib import closing

from lib.clientes import Caixa, Relatorio
from lib.memoria import RepositorioMemoria
from lib.sqlite import RepositorioSQLite


def atender(pedidos):
    caixa = Caixa(pedidos)
    caixa.vender("X-burguer", "cozinha", 18.0)
    caixa.vender("suco de laranja", "bar", 7.5)
    caixa.vender("misto quente", "cozinha", 12.0)
    Relatorio(pedidos).imprimir()


def main():
    print("== com RepositorioMemoria ==")
    atender(RepositorioMemoria())

    print("== com RepositorioSQLite ==")
    with closing(sqlite3.connect(":memory:")) as conexao:
        atender(RepositorioSQLite(conexao))


if __name__ == "__main__":
    main()
