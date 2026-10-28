from abc import ABC, abstractmethod


class Dispositivo(ABC):
    @abstractmethod
    def ler(self):
        """Devolve a medição do equipamento."""

    @abstractmethod
    def ligar(self):
        """Liga o equipamento."""

    @abstractmethod
    def desligar(self):
        """Desliga o equipamento."""


class SensorTemperatura(Dispositivo):
    def ler(self):
        return 25.5

    def ligar(self):
        raise NotImplementedError("sensor não possui acionamento")

    def desligar(self):
        raise NotImplementedError("sensor não possui acionamento")


class Motor(Dispositivo):
    def ler(self):
        raise NotImplementedError("motor não possui leitura")

    def ligar(self):
        print("motor ligado")

    def desligar(self):
        print("motor desligado")


class CLP(Dispositivo):
    def ler(self):
        return 50.0

    def ligar(self):
        print("CLP: saída ligada")

    def desligar(self):
        print("CLP: saída desligada")


def coletar_medicoes(dispositivos):
    for dispositivo in dispositivos:
        print(f"{type(dispositivo).__name__}: {dispositivo.ler()}")


def main():
    dispositivos = [SensorTemperatura(), CLP(), Motor()]
    try:
        coletar_medicoes(dispositivos)
    except NotImplementedError as erro:
        print(f"falhou: {erro}")


if __name__ == "__main__":
    main()
