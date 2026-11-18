from lib.observador import Observador
from lib.evento import PedidoPronto


class Cozinha:
    """Sujeito: guarda os inscritos e os notifica, sem saber quem são."""

    def __init__(self):
        self._prontos = set()  # estado: pedidos já prontos
        self._observadores = []

    def assinar(self, observador: Observador):
        self._observadores.append(observador)

    def concluir(self, numero):
        if numero in self._prontos:
            return  # já estava pronto: nada mudou, nenhum evento
        self._prontos.add(numero)
        print(f"cozinha: pedido {numero} pronto")
        for observador in self._observadores:
            observador.receber(PedidoPronto(numero))
