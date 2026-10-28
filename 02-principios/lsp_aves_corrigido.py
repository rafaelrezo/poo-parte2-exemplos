class Ave:
    def __init__(self, nome):
        self.nome = nome

    def comer(self):
        return f"{self.nome} está comendo"


class AveQueVoa(Ave):
    def voar(self):
        return f"{self.nome} está voando"


class Papagaio(AveQueVoa):
    pass


class Pinguim(Ave):
    def nadar(self):
        return f"{self.nome} está nadando"


def alimentar_todas(aves: list[Ave]):
    for ave in aves:
        print(ave.comer())


def soltar_todas(aves: list[AveQueVoa]):
    for ave in aves:
        print(ave.voar())


def main():
    louro = Papagaio("Louro")
    pingo = Pinguim("Pingo")
    alimentar_todas([louro, pingo])
    soltar_todas([louro])
    print(pingo.nadar())


if __name__ == "__main__":
    main()
