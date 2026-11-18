import math


class Medicao:
    def __init__(self, valor):
        self._valor = None
        if not self.atualizar(valor):
            raise ValueError("medicao inicial invalida")

    def atualizar(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            return False
        if not math.isfinite(valor) or not 0 <= valor <= 100:
            return False
        self._valor = valor
        return True

    @property
    def valor(self):
        return self._valor
