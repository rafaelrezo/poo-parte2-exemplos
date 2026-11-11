import math
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class EstadoRecebido:
    disponivel: bool
    idade_segundos: float
    alarme_ativo: bool


class Situacao(Enum):
    INDISPONIVEL = "INDISPONIVEL"
    OBSOLETO = "OBSOLETO"
    ALARME = "ALARME"
    NORMAL = "NORMAL"


def classificar(estado):
    if not estado.disponivel:
        return Situacao.INDISPONIVEL
    if not math.isfinite(estado.idade_segundos) or estado.idade_segundos < 0:
        raise ValueError("idade invalida")
    if estado.idade_segundos > 5:
        return Situacao.OBSOLETO
    if estado.alarme_ativo:
        return Situacao.ALARME
    return Situacao.NORMAL


def main():
    casos = [
        (EstadoRecebido(True, 5, False), Situacao.NORMAL),
        (EstadoRecebido(True, 5, True), Situacao.ALARME),
        (EstadoRecebido(True, 6, True), Situacao.OBSOLETO),
        (EstadoRecebido(False, 0, False), Situacao.INDISPONIVEL),
    ]
    for estado, esperado in casos:
        resultado = classificar(estado)
        assert resultado == esperado
        print(resultado.value)


if __name__ == "__main__":
    main()
