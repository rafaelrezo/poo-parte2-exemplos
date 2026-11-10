from enum import Enum


class TipoAlarme(Enum):
    NIVEL_ALTO = 1
    FORA_DA_FAIXA = 2


class Monitor:
    def __init__(self, tipo):
        self._tipo = tipo

    def avaliar(self, nivel):
        if self._tipo == TipoAlarme.NIVEL_ALTO:
            return nivel > 80
        return nivel < 20 or nivel > 80


def main():
    alto = Monitor(TipoAlarme.NIVEL_ALTO)
    faixa = Monitor(TipoAlarme.FORA_DA_FAIXA)
    assert not alto.avaliar(10)
    assert faixa.avaliar(10)
    assert not alto.avaliar(80)
    assert not faixa.avaliar(80)
    print(f"nivel 10: alto={str(alto.avaliar(10)).lower()}, "
          f"faixa={str(faixa.avaliar(10)).lower()}")


if __name__ == "__main__":
    main()
