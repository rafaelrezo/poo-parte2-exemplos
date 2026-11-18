import unittest

from planta.medicao import Medicao


class TestMedicao(unittest.TestCase):
    def test_valor_inicial_e_fronteiras(self):
        medicao = Medicao(50)
        self.assertEqual(medicao.valor, 50)
        self.assertTrue(medicao.atualizar(0))
        self.assertTrue(medicao.atualizar(100))
        self.assertEqual(medicao.valor, 100)

    def test_rejeicao_preserva_ultimo_valor(self):
        medicao = Medicao(50)
        self.assertFalse(medicao.atualizar(-1))
        self.assertEqual(medicao.valor, 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
