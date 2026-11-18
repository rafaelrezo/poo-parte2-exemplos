class Cozinha:
    """Receptor: sabe preparar lanches; não sabe que existe uma fila."""

    def preparar_lanche(self, numero, lanche):
        print(f"  cozinha: {lanche} (pedido {numero})")


class Bar:
    """Receptor: sabe preparar bebidas."""

    def preparar_bebida(self, numero, bebida):
        print(f"  bar: {bebida} (pedido {numero})")
