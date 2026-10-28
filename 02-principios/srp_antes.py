class SensorTemperatura:
    def __init__(self, limite):
        self._limite = limite
        self.registros = []

    def ler(self):
        return 92.5  # valor simulado

    def verificar(self):
        temperatura = self.ler()
        self.registros.append(temperatura)
        if temperatura > self._limite:
            print(f"[e-mail para operador@planta] ALERTA: {temperatura} °C")
        return temperatura


def main():
    sensor = SensorTemperatura(limite=90)
    sensor.verificar()
    print(f"registros: {sensor.registros}")


if __name__ == "__main__":
    main()
