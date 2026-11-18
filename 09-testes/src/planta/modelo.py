import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Aquisicao:
    sessao: str
    ciclo: int
    nivel: float

    def __post_init__(self):
        if not isinstance(self.sessao, str) or not self.sessao.strip():
            raise ValueError("sessao invalida")
        if type(self.ciclo) is not int or self.ciclo <= 0:
            raise ValueError("ciclo invalido")
        if (type(self.nivel) not in (int, float) or not 0 <= self.nivel <= 100
                or not math.isfinite(self.nivel)):
            raise ValueError("nivel invalido")
