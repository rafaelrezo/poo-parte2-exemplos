import sqlite3
import unittest
from contextlib import closing

from lib.clientes import Caixa
from lib.memoria import RepositorioMemoria
from lib.modelo import Pedido
from lib.sqlite import RepositorioSQLite


class TestRepositorio(unittest.TestCase):
    def verificar_contrato(self, pedidos):
        self.assertEqual(pedidos.ultimo_numero(), 0)
        self.assertIsNone(pedidos.buscar(1))

        lanche = Pedido(1, "X-burguer", "cozinha", 18.0)
        self.assertTrue(pedidos.adicionar(lanche))
        self.assertFalse(pedidos.adicionar(lanche))
        self.assertTrue(pedidos.adicionar(Pedido(2, "suco de laranja", "bar", 7.5)))
        self.assertEqual(pedidos.buscar(1), lanche)
        self.assertEqual(pedidos.ultimo_numero(), 2)
        self.assertEqual(
            pedidos.faturamento_por_setor(), {"bar": 7.5, "cozinha": 18.0}
        )

    def test_memoria(self):
        self.verificar_contrato(RepositorioMemoria())

    def test_sqlite(self):
        with closing(sqlite3.connect(":memory:")) as conexao:
            self.verificar_contrato(RepositorioSQLite(conexao))

    def test_caixa_sem_banco(self):
        pedidos = RepositorioMemoria()
        pedidos.adicionar(Pedido(41, "pastel", "cozinha", 9.0))
        numero = Caixa(pedidos).vender("X-burguer", "cozinha", 18.0)
        self.assertEqual(numero, 42)
        self.assertEqual(pedidos.buscar(42).item, "X-burguer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
