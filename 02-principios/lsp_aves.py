class Ave:
    def __init__(self, nome):
        self.nome = nome

    def voar(self):
        return f"{self.nome} está voando"


class Papagaio(Ave):
    pass


class Pinguim(Ave):
    def voar(self):
        raise NotImplementedError(f"{self.nome} é um pinguim e não voa")


def soltar_todas(aves):
    for ave in aves:
        print(ave.voar())


def main():
    aves = [Papagaio("Louro"), Pinguim("Pingo")]
    try:
        soltar_todas(aves)
    except NotImplementedError as erro:
        print(f"falhou: {erro}")


if __name__ == "__main__":
    main()
