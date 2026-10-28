class SensorNivel:
    def __init__(self):
        self.percentual = 90


class PainelEstacao:
    def __init__(self):
        self._sensor = SensorNivel()

    def executar(self):
        alerta = self._sensor.percentual > 80
        estado = "ALERTA" if alerta else "NORMAL"
        print(f"LT-01: {estado}")


def main():
    painel = PainelEstacao()
    painel.executar()


if __name__ == "__main__":
    main()
