from lib.frete import Frete


class Pedido:
    """Contexto: cuida do pedido e delega o cálculo do frete."""

    def __init__(self, produtos, peso_kg, frete: Frete):
        if produtos < 0 or peso_kg <= 0 or frete is None:
            raise ValueError("pedido com valor, peso ou frete inválido")
        self._produtos = produtos
        self._peso_kg = peso_kg
        self._frete = frete

    def frete(self):
        return self._frete.calcular(self._peso_kg)

    def total(self):
        return self._produtos + self.frete()
