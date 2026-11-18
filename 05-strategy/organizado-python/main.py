from lib.montagem import criar_frete
from lib.pedido import Pedido


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
