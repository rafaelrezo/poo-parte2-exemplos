from command import Comando, Cozinha, Fila, PrepararLanche  # command.py não é modificado


class Confeitaria:
    """Receptor novo: a lanchonete passou a vender sobremesas."""

    def __init__(self):
        self.feitas = []

    def montar_sobremesa(self, numero, sobremesa):
        self.feitas.append(numero)
        print(f"  confeitaria: {sobremesa} (pedido {numero})")


class PrepararSobremesa(Comando):
    """Comando novo: liga a solicitação ao receptor novo."""

    def __init__(self, confeitaria, numero, sobremesa):
        self._confeitaria = confeitaria
        self._numero = numero
        self._sobremesa = sobremesa

    def executar(self):
        self._confeitaria.montar_sobremesa(self._numero, self._sobremesa)

    def descrever(self):
        return f"pedido {self._numero}: {self._sobremesa} na confeitaria"


def testar_comanda_isolada():
    # Prepara: o receptor e a comanda, sem fila e sem caixa
    confeitaria = Confeitaria()
    comanda = PrepararSobremesa(confeitaria, 9, "pudim")
    # Executa: nada acontece até alguém chamar executar
    assert confeitaria.feitas == []
    comanda.executar()
    # Confere: o pedido chegou ao receptor certo e a descrição o identifica
    assert confeitaria.feitas == [9]
    assert comanda.descrever() == "pedido 9: pudim na confeitaria"
    print("teste da comanda isolada: ok")


def main():
    testar_comanda_isolada()
    cozinha = Cozinha()
    confeitaria = Confeitaria()
    fila = Fila()  # a mesma Fila de antes
    fila.receber(PrepararLanche(cozinha, 1, "X-burguer"))
    fila.receber(PrepararSobremesa(confeitaria, 2, "pudim"))
    fila.atender_todos()
    print("historico da fila:")
    for linha in fila.historico:
        print(f"  {linha}")


if __name__ == "__main__":
    main()
