from abc import ABC, abstractmethod


class PoliticaAlarme(ABC):
    @abstractmethod
    def aciona(self, nivel):
        raise NotImplementedError


class NivelAlto(PoliticaAlarme):
    def aciona(self, nivel):
        return nivel > 80


class ForaDaFaixa(PoliticaAlarme):
    def aciona(self, nivel):
        return nivel < 20 or nivel > 80


class Monitor:
    def __init__(self, politica):
        self._politica = politica

    def avaliar(self, nivel):
        return self._politica.aciona(nivel)


def main():
    alto = Monitor(NivelAlto())
    faixa = Monitor(ForaDaFaixa())
    assert not alto.avaliar(10)
    assert faixa.avaliar(10)
    assert not alto.avaliar(80)
    assert not faixa.avaliar(80)
    print(f"nivel 10: alto={str(alto.avaliar(10)).lower()}, "
          f"faixa={str(faixa.avaliar(10)).lower()}")


if __name__ == "__main__":
    main()
