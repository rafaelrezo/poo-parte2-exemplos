from lib.cozinha import Cozinha
from lib.observadores import Aplicativo, Painel


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
