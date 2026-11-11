from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PedidoPronto:
    """Evento: o que aconteceu, com os dados que os interessados precisam."""

    numero: int


class Observador(ABC):
    """Observador: o contrato de quem quer ser avisado."""

    @abstractmethod
    def receber(self, evento):
        """Reage a um evento publicado pela cozinha."""


class Cozinha:
    """Sujeito: guarda os inscritos e os notifica, sem saber quem são."""

    def __init__(self):
        self._prontos = set()  # estado: pedidos já prontos
        self._observadores = []

    def assinar(self, observador):
        self._observadores.append(observador)

    def concluir(self, numero):
        if numero in self._prontos:
            return  # já estava pronto: nada mudou, nenhum evento
        self._prontos.add(numero)
        print(f"cozinha: pedido {numero} pronto")
        for observador in self._observadores:
            observador.receber(PedidoPronto(numero))


class Painel(Observador):
    def receber(self, evento):
        print(f"  painel: PRONTO {evento.numero}")


class Aplicativo(Observador):
    def receber(self, evento):
        print(f"  app: pedido {evento.numero} pronto, pode retirar")


def main():
    painel = Painel()
    app = Aplicativo()
    cozinha = Cozinha()
    cozinha.assinar(painel)
    cozinha.assinar(app)

    cozinha.concluir(1)
    cozinha.concluir(2)
    print("(o cozinheiro aperta de novo o botao do pedido 2)")
    cozinha.concluir(2)


if __name__ == "__main__":
    main()
