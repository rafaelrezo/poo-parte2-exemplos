from abc import ABC, abstractmethod


class Sensor(ABC):
    """Abstração definida pelo módulo de alto nível: o que o controle precisa."""

    @abstractmethod
    def ler(self):
        """Temperatura em °C."""


class ControladorTemperatura:
    def __init__(self, sensor, limite):
        self._sensor = sensor
        self._limite = limite

    def decidir(self):
        if self._sensor.ler() > self._limite:
            return "ligar resfriamento"
        return "manter"


class SensorModbus(Sensor):
    def __init__(self, endereco):
        self._endereco = endereco

    def ler(self):
        raise ConnectionError(f"sem resposta de {self._endereco}")


class SensorSimulado(Sensor):
    def __init__(self, valor):
        self._valor = valor

    def ler(self):
        return self._valor


def main():
    for valor in (89, 90, 91):
        controlador = ControladorTemperatura(SensorSimulado(valor), limite=90)
        print(f"simulado {valor} °C -> {controlador.decidir()}")

    producao = ControladorTemperatura(SensorModbus("192.168.0.10:502"), limite=90)
    try:
        print(producao.decidir())
    except ConnectionError as erro:
        print(f"produção sem equipamento: {erro}")


if __name__ == "__main__":
    main()
