from abc import ABC, abstractmethod


class Frete(ABC):
    """Estratégia: o contrato comum a todas as modalidades de frete."""

    @abstractmethod
    def calcular(self, peso_kg):
        """Recebe o peso em kg e devolve o valor do frete em reais."""


class Retirada(Frete):
    def calcular(self, peso_kg):
        return 0.0


class PorPeso(Frete):
    def calcular(self, peso_kg):
        return 8.0 + 4.0 * peso_kg


class PorFaixa(Frete):
    def calcular(self, peso_kg):
        if peso_kg <= 1.0:
            return 15.0
        if peso_kg <= 5.0:
            return 25.0
        return 35.0


class Pedido:
    """Contexto: cuida do pedido e delega o cálculo do frete."""

    def __init__(self, produtos, peso_kg, frete):
        if produtos < 0 or peso_kg <= 0 or frete is None:
            raise ValueError("pedido com valor, peso ou frete inválido")
        self._produtos = produtos
        self._peso_kg = peso_kg
        self._frete = frete

    def frete(self):
        return self._frete.calcular(self._peso_kg)

    def total(self):
        return self._produtos + self.frete()


def criar_frete(nome):
    """Montagem: o único lugar que conhece as modalidades concretas."""
    if nome == "retirada":
        return Retirada()
    if nome == "por_peso":
        return PorPeso()
    if nome == "por_faixa":
        return PorFaixa()
    raise ValueError(f"modalidade de frete desconhecida: {nome}")


def main():
    print("peso  retirada  por_peso  por_faixa")
    for peso in (0.5, 3.0, 8.0):
        retirada = Pedido(100.0, peso, criar_frete("retirada"))
        por_peso = Pedido(100.0, peso, criar_frete("por_peso"))
        por_faixa = Pedido(100.0, peso, criar_frete("por_faixa"))
        print(f"{peso:4.1f}  {retirada.frete():8.2f}  "
              f"{por_peso.frete():8.2f}  {por_faixa.frete():9.2f}")
    exemplo = Pedido(100.0, 3.0, criar_frete("por_peso"))
    print(f"total de um pedido de 100.00 com 3 kg, por peso: {exemplo.total():.2f}")


if __name__ == "__main__":
    main()
