class SensorModbus:
    """Lê um transmissor por Modbus TCP. Nesta aula não há equipamento:
    a classe só representa a tentativa de comunicação."""

    def __init__(self, endereco):
        self._endereco = endereco

    def ler(self):
        raise ConnectionError(f"sem resposta de {self._endereco}")


class ControladorTemperatura:
    def __init__(self):
        self._sensor = SensorModbus("192.168.0.10:502")  # detalhe fixado no código
        self._limite = 90

    def decidir(self):
        if self._sensor.ler() > self._limite:
            return "ligar resfriamento"
        return "manter"


def main():
    controlador = ControladorTemperatura()
    try:
        print(controlador.decidir())
    except ConnectionError as erro:
        print(f"não foi possível testar a regra: {erro}")


if __name__ == "__main__":
    main()
