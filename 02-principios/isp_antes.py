from abc import ABC, abstractmethod


class DispositivoIndustrial(ABC):
    @abstractmethod
    def ler_temperatura(self):
        """Temperatura em °C."""

    @abstractmethod
    def acionar_motor(self, ligado):
        """Liga ou desliga o motor do dispositivo."""

    @abstractmethod
    def enviar_notificacao(self, mensagem):
        """Avisa o operador."""


class SensorPT100(DispositivoIndustrial):
    def ler_temperatura(self):
        return 72.0

    def acionar_motor(self, ligado):
        raise NotImplementedError("um sensor não tem motor")

    def enviar_notificacao(self, mensagem):
        raise NotImplementedError("um sensor não envia mensagens")


def exibir_temperatura(dispositivo):
    print(f"temperatura: {dispositivo.ler_temperatura()} °C")


def desligar_todos(dispositivos):
    for dispositivo in dispositivos:
        dispositivo.acionar_motor(False)


def main():
    sensor = SensorPT100()
    exibir_temperatura(sensor)
    try:
        desligar_todos([sensor])
    except NotImplementedError as erro:
        print(f"falha ao desligar: {erro}")


if __name__ == "__main__":
    main()
