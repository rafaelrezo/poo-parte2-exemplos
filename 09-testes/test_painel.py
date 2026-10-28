import os
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from streamlit.testing.v1 import AppTest
from repository import Aquisicao, HistoricoSQLite


class TestPainel(unittest.TestCase):
    def test_banco_ausente_e_tabela(self):
        aplicativo = Path(__file__).resolve().parent / "painel.py"
        anterior = Path.cwd()
        with TemporaryDirectory() as pasta:
            try:
                os.chdir(pasta)
                tela = AppTest.from_file(str(aplicativo)).run(timeout=10)
                self.assertFalse(tela.exception)
                self.assertEqual(len(tela.info), 1)
                conexao = sqlite3.connect("historico.db")
                try:
                    HistoricoSQLite(conexao).salvar(Aquisicao("ensaio", 1, 48.5))
                finally:
                    conexao.close()
                tela.run(timeout=10)
                self.assertFalse(tela.exception)
                self.assertEqual(len(tela.dataframe), 1)
                self.assertEqual(float(tela.dataframe[0].value.iloc[0]["nivel"]), 48.5)
            finally:
                os.chdir(anterior)


if __name__ == "__main__":
    unittest.main(verbosity=2)
