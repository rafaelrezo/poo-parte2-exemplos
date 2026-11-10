from enum import Enum


class TipoFrete(Enum):
    RETIRADA = 1
    POR_PESO = 2
    POR_FAIXA = 3


class Pedido:
    def __init__(self, produtos, peso_kg, tipo):
        if produtos < 0 or peso_kg <= 0:
            raise ValueError("pedido com valor ou peso inválido")
        self._produtos = produtos
        self._peso_kg = peso_kg
        self._tipo = tipo

    def frete(self):
        if self._tipo == TipoFrete.RETIRADA:
            return 0.0
        if self._tipo == TipoFrete.POR_PESO:
            return 8.0 + 4.0 * self._peso_kg
        # TipoFrete.POR_FAIXA
        if self._peso_kg <= 1.0:
            return 15.0
        if self._peso_kg <= 5.0:
            return 25.0
        return 35.0

    def total(self):
        return self._produtos + self.frete()


def main():
    print("peso  retirada  por_peso  por_faixa")
    for peso in (0.5, 3.0, 8.0):
        retirada = Pedido(100.0, peso, TipoFrete.RETIRADA)
        por_peso = Pedido(100.0, peso, TipoFrete.POR_PESO)
        por_faixa = Pedido(100.0, peso, TipoFrete.POR_FAIXA)
        print(f"{peso:4.1f}  {retirada.frete():8.2f}  "
              f"{por_peso.frete():8.2f}  {por_faixa.frete():9.2f}")
    exemplo = Pedido(100.0, 3.0, TipoFrete.POR_PESO)
    print(f"total de um pedido de 100.00 com 3 kg, por peso: {exemplo.total():.2f}")


if __name__ == "__main__":
    main()
