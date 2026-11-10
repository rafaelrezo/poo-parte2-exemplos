from strategy import Frete, Pedido  # strategy.py não é modificado


class Motoboy(Frete):
    """Modalidade nova: preço fixo até 10 kg; acima disso, a moto não leva."""

    def calcular(self, peso_kg):
        if peso_kg > 10.0:
            raise ValueError("motoboy só leva pedidos de até 10 kg")
        return 12.0


def testar_motoboy_isolado():
    # Prepara: a modalidade sozinha, sem pedido
    motoboy = Motoboy()
    # Executa e confere: preço fixo dentro do limite, recusa acima dele
    assert motoboy.calcular(0.5) == 12.0
    assert motoboy.calcular(10.0) == 12.0
    try:
        motoboy.calcular(10.5)
        assert False, "deveria recusar 10.5 kg"
    except ValueError:
        pass
    print("teste do motoboy isolado: ok")


def main():
    testar_motoboy_isolado()
    pedido = Pedido(100.0, 3.0, Motoboy())  # o mesmo Pedido de antes
    print(f"pedido de 100.00 com 3 kg, motoboy: frete {pedido.frete():.2f}, "
          f"total {pedido.total():.2f}")


if __name__ == "__main__":
    main()
