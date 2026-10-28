from abc import ABC, abstractmethod


class Forma(ABC):
    @abstractmethod
    def area(self):
        """Área da figura."""


class Retangulo(Forma):
    def __init__(self, largura, altura):
        self._largura = largura
        self._altura = altura

    def area(self):
        return self._largura * self._altura


class Quadrado(Forma):
    def __init__(self, lado):
        self._lado = lado

    def area(self):
        return self._lado * self._lado


def area_total(formas):
    return sum(forma.area() for forma in formas)


def main():
    formas = [Retangulo(2, 3), Quadrado(3)]
    for forma in formas:
        print(f"{type(forma).__name__:9} área {forma.area()}")
    print(f"área total: {area_total(formas)}")


if __name__ == "__main__":
    main()
