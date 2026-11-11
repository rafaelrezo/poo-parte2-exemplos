class Cozinha:
    def preparar_lanche(self, numero, lanche):
        print(f"  cozinha: {lanche} (pedido {numero})")


class Bar:
    def preparar_bebida(self, numero, bebida):
        print(f"  bar: {bebida} (pedido {numero})")


class Caixa:
    def __init__(self, cozinha, bar):
        self._cozinha = cozinha
        self._bar = bar
        self._numero = 0

    def vender_lanche(self, lanche):
        self._numero += 1
        self._cozinha.preparar_lanche(self._numero, lanche)
        print(f"caixa: pedido {self._numero} entregue, proximo cliente")

    def vender_bebida(self, bebida):
        self._numero += 1
        self._bar.preparar_bebida(self._numero, bebida)
        print(f"caixa: pedido {self._numero} entregue, proximo cliente")


def main():
    cozinha = Cozinha()
    bar = Bar()
    caixa = Caixa(cozinha, bar)
    caixa.vender_lanche("X-burguer")
    caixa.vender_bebida("suco de laranja")
    caixa.vender_lanche("misto quente")


if __name__ == "__main__":
    main()
