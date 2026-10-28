class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def mudar_largura(self, largura):
        self.largura = largura

    def area(self):
        return self.largura * self.altura


class Quadrado(Retangulo):
    def __init__(self, lado):
        super().__init__(lado, lado)

    def mudar_largura(self, largura):
        self.largura = largura
        self.altura = largura  # num quadrado, os lados continuam iguais


def dobrar_largura(figura):
    antes = figura.area()
    figura.mudar_largura(figura.largura * 2)
    print(f"{type(figura).__name__:9} área {antes} -> {figura.area()}")


def main():
    dobrar_largura(Retangulo(2, 3))
    dobrar_largura(Quadrado(3))


if __name__ == "__main__":
    main()
