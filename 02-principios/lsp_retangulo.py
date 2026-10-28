class Retangulo:
    def __init__(self, largura, altura):
        self._largura = largura
        self._altura = altura

    def definir_largura(self, largura):
        self._largura = largura

    def definir_altura(self, altura):
        self._altura = altura

    def area(self):
        return self._largura * self._altura


class Quadrado(Retangulo):
    def __init__(self, lado):
        super().__init__(lado, lado)

    def definir_largura(self, largura):
        self._largura = largura
        self._altura = largura  # mantém os lados iguais

    def definir_altura(self, altura):
        self._largura = altura
        self._altura = altura


def preparar_etiqueta(retangulo):
    """Espera um retângulo de 5 x 4, com área 20."""
    retangulo.definir_largura(5)
    retangulo.definir_altura(4)
    return retangulo.area()


def main():
    for forma in (Retangulo(1, 1), Quadrado(1)):
        print(f"{type(forma).__name__:9} área esperada 20, obtida {preparar_etiqueta(forma)}")


if __name__ == "__main__":
    main()
