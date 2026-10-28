import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repository import Aquisicao, HistoricoSQLite, exportar_csv


class TestHistorico(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name) / "historico.db"
        self.conexao = sqlite3.connect(self.caminho)
        self.addCleanup(self.conexao.close)
        self.historico = HistoricoSQLite(self.conexao)

    def test_repeticao_e_nova_sessao(self):
        aquisicao = Aquisicao("ensaio", 1, 48.5)
        self.assertTrue(self.historico.salvar(aquisicao))
        self.assertFalse(self.historico.salvar(aquisicao))
        self.assertTrue(self.historico.salvar(Aquisicao("reinicio", 1, 49.0)))
        self.assertEqual(len(self.historico.listar()), 2)

    def test_conflito_preserva_original(self):
        original = Aquisicao("ensaio", 1, 48.5)
        self.historico.salvar(original)
        with self.assertRaisesRegex(ValueError, "conteudo diferente"):
            self.historico.salvar(Aquisicao("ensaio", 1, 99))
        self.assertEqual(self.historico.listar(), [original])
        self.assertTrue(self.historico.salvar(Aquisicao("ensaio", 2, 49)))

    def test_persistencia_apos_reabrir(self):
        original = Aquisicao("ensaio", 1, 48.5)
        self.historico.salvar(original)
        self.conexao.close()
        with sqlite3.connect(self.caminho) as outra:
            self.addCleanup(outra.close)
            self.assertEqual(HistoricoSQLite(outra).listar(), [original])

    def test_fronteiras_e_rejeicao(self):
        for valor in [0, 100]:
            with self.subTest(valor=valor):
                self.assertEqual(Aquisicao("ensaio", 1, valor).nivel, valor)
        for valor in [-1, 101, True, "48.5", float("nan"), float("inf")]:
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    Aquisicao("ensaio", 1, valor)

    def test_csv_corresponde_a_consulta(self):
        self.historico.salvar(Aquisicao("ensaio", 1, 48.5))
        texto = exportar_csv(self.historico.listar())
        self.assertEqual(texto, "sessao,ciclo,nivel\nensaio,1,48.5\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
