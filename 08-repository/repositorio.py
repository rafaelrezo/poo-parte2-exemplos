import sqlite3
from abc import ABC, abstractmethod
from contextlib import closing
from dataclasses import dataclass


@dataclass(frozen=True)
class Pedido:
    """Entidade: o objeto do domínio que o repositório guarda."""

    numero: int
    item: str
    setor: str
    valor: float


class RepositorioPedidos(ABC):
    """Repositório: o contrato que o domínio conhece, escrito na linguagem do domínio."""

    @abstractmethod
    def adicionar(self, pedido):
        """Guarda o pedido; devolve False se o número já existia."""

    @abstractmethod
    def buscar(self, numero):
        """Devolve o Pedido com esse número, ou None."""

    @abstractmethod
    def ultimo_numero(self):
        """Maior número guardado, ou 0 se não houver pedidos."""

    @abstractmethod
    def faturamento_por_setor(self):
        """Dicionário {setor: total vendido}."""


class RepositorioMemoria(RepositorioPedidos):
    """Implementação em memória: rápida, sem arquivo, perde tudo ao terminar."""

    def __init__(self):
        self._pedidos = {}

    def adicionar(self, pedido):
        if pedido.numero in self._pedidos:
            return False
        self._pedidos[pedido.numero] = pedido
        return True

    def buscar(self, numero):
        return self._pedidos.get(numero)

    def ultimo_numero(self):
        return max(self._pedidos, default=0)

    def faturamento_por_setor(self):
        totais = {}
        for pedido in self._pedidos.values():
            totais[pedido.setor] = totais.get(pedido.setor, 0) + pedido.valor
        return dict(sorted(totais.items()))


class RepositorioSQLite(RepositorioPedidos):
    """Implementação com SQLite: todo o SQL do programa fica nesta classe."""

    def __init__(self, conexao):
        self._conexao = conexao  # emprestada: quem abriu a conexão a fecha
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    numero INTEGER PRIMARY KEY,
                    item   TEXT    NOT NULL,
                    setor  TEXT    NOT NULL,
                    valor  REAL    NOT NULL CHECK (valor > 0)
                )
            """)

    def adicionar(self, pedido):
        with self._conexao:
            cursor = self._conexao.execute("""
                INSERT INTO pedidos (numero, item, setor, valor) VALUES (?, ?, ?, ?)
                ON CONFLICT (numero) DO NOTHING
            """, (pedido.numero, pedido.item, pedido.setor, pedido.valor))
        return cursor.rowcount == 1

    def buscar(self, numero):
        linha = self._conexao.execute(
            "SELECT numero, item, setor, valor FROM pedidos WHERE numero = ?", (numero,)
        ).fetchone()
        return Pedido(*linha) if linha else None

    def ultimo_numero(self):
        return self._conexao.execute("SELECT COALESCE(MAX(numero), 0) FROM pedidos").fetchone()[0]

    def faturamento_por_setor(self):
        linhas = self._conexao.execute(
            "SELECT setor, SUM(valor) FROM pedidos GROUP BY setor ORDER BY setor"
        ).fetchall()
        return dict(linhas)


class Caixa:
    """Cliente: registra vendas; conhece só o contrato RepositorioPedidos."""

    def __init__(self, pedidos):
        self._pedidos = pedidos

    def vender(self, item, setor, valor):
        pedido = Pedido(self._pedidos.ultimo_numero() + 1, item, setor, valor)
        self._pedidos.adicionar(pedido)
        print(f"caixa: pedido {pedido.numero} registrado")
        return pedido.numero


class Relatorio:
    """Cliente: apresenta o faturamento; também não conhece SQL."""

    def __init__(self, pedidos):
        self._pedidos = pedidos

    def imprimir(self):
        print("faturamento por setor:")
        for setor, total in self._pedidos.faturamento_por_setor().items():
            print(f"  {setor}: R$ {total:.2f}")


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
