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

    def concluir(self, numero):
        print(f"cozinha: pedido {numero} pronto")
        self._painel.mostrar_pronto(numero)
        self._app.avisar_cliente(numero)


def main():
    painel = Painel()
    app = Aplicativo()
    cozinha = Cozinha(painel, app)
    cozinha.concluir(1)
    cozinha.concluir(2)


if __name__ == "__main__":
    main()
