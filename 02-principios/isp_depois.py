from abc import ABC, abstractmethod


class LeitorTemperatura(ABC):
    @abstractmethod
    def ler_temperatura(self):
        """Temperatura em °C."""


class AtuadorMotor(ABC):
    @abstractmethod
    def ligar(self):
        """Liga o motor."""

    @abstractmethod
    def desligar(self):
        """Desliga o motor."""


class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem):
        """Avisa o operador."""


class SensorPT100(LeitorTemperatura):
    def ler_temperatura(self):
        return 72.0


class InversorBomba(AtuadorMotor, LeitorTemperatura):
    """Um dispositivo real pode ter duas capacidades: aciona o motor e mede sua temperatura."""

    def __init__(self):
        self._ligado = False

    def ligar(self):
        self._ligado = True
        print("bomba ligada")

    def desligar(self):
        self._ligado = False
        print("bomba desligada")

    def ler_temperatura(self):
        return 55.0 if self._ligado else 30.0


class NotificadorConsole(Notificador):
    def enviar(self, mensagem):
        print(f"[aviso] {mensagem}")


def exibir_temperatura(leitor):
    print(f"temperatura: {leitor.ler_temperatura()} °C")


def desligar_todos(motores):
    for motor in motores:
        motor.desligar()


def main():
    sensor = SensorPT100()
    inversor = InversorBomba()
    exibir_temperatura(sensor)
    inversor.ligar()
    exibir_temperatura(inversor)
    desligar_todos([inversor])
    NotificadorConsole().enviar("ciclo concluído")


if __name__ == "__main__":
    main()
