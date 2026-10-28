import subprocess
import unittest
from pathlib import Path

from contrato import interpretar


class TestIntegracao(unittest.TestCase):
    def test_produtor_e_consumidor(self):
        executavel = Path(__file__).resolve().parent / "produtor_fixture"
        processo = subprocess.run([str(executavel), "48.5"],
                                   capture_output=True, text=True, timeout=5)
        self.assertEqual(processo.returncode, 0, processo.stderr)
        aquisicao = interpretar(processo.stdout)
        self.assertEqual((aquisicao.sessao, aquisicao.ciclo), ("ensaio", 12))
        self.assertEqual(aquisicao.nivel, 48.5)

    def test_produtor_recusa_numero_invalido(self):
        executavel = Path(__file__).resolve().parent / "produtor_fixture"
        processo = subprocess.run([str(executavel), "nan"],
                                   capture_output=True, text=True, timeout=5)
        self.assertNotEqual(processo.returncode, 0)
        self.assertEqual(processo.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
