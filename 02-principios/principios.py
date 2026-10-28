class ErroLeitura(Exception):
    """Falha de aquisição prevista no contrato."""


class SensorSimulado:
    def __init__(self, valor, disponivel=True):
        self._valor = valor
        self._disponivel = disponivel

    def ler(self):
        if not self._disponivel:
            raise ErroLeitura("aquisição indisponível")
        return self._valor


class ControladorTemperatura:
    def __init__(self, sensor, limite):
        self._sensor = sensor
        self._limite = limite

    def decidir(self):
        if self._sensor.ler() > self._limite:
            return "ligar resfriamento"
        return "manter"


def main():
    for valor, esperado in [(89, "manter"), (90, "manter"), (91, "ligar resfriamento")]:
        controlador = ControladorTemperatura(SensorSimulado(valor), limite=90)
        assert controlador.decidir() == esperado, f"{valor} °C deveria resultar em {esperado}"

    controlador = ControladorTemperatura(SensorSimulado(0, disponivel=False), limite=90)
    try:
        controlador.decidir()
    except ErroLeitura:
        pass
    else:
        raise AssertionError("a falha de leitura deveria ser propagada")

    print("OK: abaixo, igualdade, acima e falha")


if __name__ == "__main__":
    main()
