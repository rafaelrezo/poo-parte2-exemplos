from abc import ABC, abstractmethod


class ErroLeitura(Exception):
    """Falha de aquisição prevista no contrato."""


class Sensor(ABC):
    @abstractmethod
    def ler(self):
        """Contrato:
        - pré-condição: nenhuma; o sensor pode ser lido a qualquer momento;
        - pós-condição: devolve a temperatura em °C;
        - falha: lança ErroLeitura quando não consegue medir.
        """


class SensorSimulado(Sensor):
    def __init__(self, valor):
        self._valor = valor

    def ler(self):
        return self._valor


class SensorSemComunicacao(Sensor):
    def ler(self):
        raise ErroLeitura("sem resposta do transmissor")  # falha prevista: válido


class SensorKelvin(Sensor):
    def ler(self):
        return 338.15  # 65 °C em kelvin: viola a pós-condição


def verificar(sensor, limite=90):
    try:
        temperatura = sensor.ler()
    except ErroLeitura as erro:
        return f"leitura indisponível ({erro})"
    return "ALARME" if temperatura > limite else "normal"


def main():
    for sensor in (SensorSimulado(65), SensorSemComunicacao(), SensorKelvin()):
        print(f"{type(sensor).__name__:20} -> {verificar(sensor)}")


if __name__ == "__main__":
    main()
