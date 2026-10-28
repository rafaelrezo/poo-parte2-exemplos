from abc import ABC, abstractmethod


class IFonteLeitura(ABC):
    @abstractmethod
    def valor(self):
        raise NotImplementedError


class FonteConstante(IFonteLeitura):
    def __init__(self, percentual):
        self._percentual = percentual

    def valor(self):
        return self._percentual


class PoliticaAlarme:
    def __init__(self, limite):
        self._limite = limite

    def aciona(self, valor):
        return valor > self._limite


class ControladorConsulta:
    def __init__(self, fonte, politica):
        self._fonte = fonte
        self._politica = politica

    def avaliar(self):
        return self._politica.aciona(self._fonte.valor())


def main():
    fonte = FonteConstante(90)
    politica = PoliticaAlarme(80)
    controlador = ControladorConsulta(fonte, politica)
    alerta = controlador.avaliar()
    estado = "ALERTA" if alerta else "NORMAL"
    print(f"LT-01: {estado}")


if __name__ == "__main__":
    main()
