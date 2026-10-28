from abc import ABC, abstractmethod


class Leitura(ABC):
    @abstractmethod
    def ler(self):
        """Devolve a medição do equipamento."""


class Acionamento(ABC):
    @abstractmethod
    def ligar(self):
        """Liga o equipamento."""

    @abstractmethod
    def desligar(self):
        """Desliga o equipamento."""


class SensorTemperatura(Leitura):
    def ler(self):
        return 25.5


class Motor(Acionamento):
    def ligar(self):
        print("motor ligado")

    def desligar(self):
        print("motor desligado")


class CLP(Leitura, Acionamento):
    def ler(self):
        return 50.0

    def ligar(self):
        print("CLP: saída ligada")

    def desligar(self):
        print("CLP: saída desligada")


def coletar_medicoes(leitores: list[Leitura]):
    for leitor in leitores:
        print(f"{type(leitor).__name__}: {leitor.ler()}")


def desligar_todos(equipamentos: list[Acionamento]):
    for equipamento in equipamentos:
        equipamento.desligar()


def main():
    sensor = SensorTemperatura()
    motor = Motor()
    clp = CLP()
    coletar_medicoes([sensor, clp])
    desligar_todos([motor, clp])


if __name__ == "__main__":
    main()
