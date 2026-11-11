class Painel:
    def mostrar_pronto(self, numero):
        print(f"  painel: PRONTO {numero}")


class Aplicativo:
    def avisar_cliente(self, numero):
        print(f"  app: pedido {numero} pronto, pode retirar")


class Cozinha:
    def __init__(self, painel, app):
        self._painel = painel
        self._app = app

    def preparar(self, numero, item):
        print(f"  cozinha: preparou {item}")
        self._painel.mostrar_pronto(numero)
        self._app.avisar_cliente(numero)


class Caixa:
    def __init__(self, cozinha):
        self._cozinha = cozinha
        self._numero = 0

    def vender(self, item):
        self._numero += 1
        print(f"caixa: pedido {self._numero}, {item}")
        self._cozinha.preparar(self._numero, item)
        print("caixa: pronto para o proximo cliente")


def main():
    painel = Painel()
    app = Aplicativo()
    cozinha = Cozinha(painel, app)
    caixa = Caixa(cozinha)
    caixa.vender("X-burguer")
    caixa.vender("misto quente")


if __name__ == "__main__":
    main()
