from abc import ABC, abstractmethod


class Cozinha:
    """Receptor: sabe preparar lanches; não sabe que existe uma fila."""

    def preparar_lanche(self, numero, lanche):
        print(f"  cozinha: {lanche} (pedido {numero})")


class Bar:
    """Receptor: sabe preparar bebidas."""

    def preparar_bebida(self, numero, bebida):
        print(f"  bar: {bebida} (pedido {numero})")


class Comando(ABC):
    """Comando: o contrato comum de toda solicitação."""

    @abstractmethod
    def executar(self):
        """Encaminha a solicitação ao seu receptor."""

    @abstractmethod
    def descrever(self):
        """Texto curto que identifica a solicitação no histórico."""


class PrepararLanche(Comando):
    def __init__(self, cozinha, numero, lanche):
        self._cozinha = cozinha
        self._numero = numero
        self._lanche = lanche

    def executar(self):
        self._cozinha.preparar_lanche(self._numero, self._lanche)

    def descrever(self):
        return f"pedido {self._numero}: {self._lanche} na cozinha"


class PrepararBebida(Comando):
    def __init__(self, bar, numero, bebida):
        self._bar = bar
        self._numero = numero
        self._bebida = bebida

    def executar(self):
        self._bar.preparar_bebida(self._numero, self._bebida)

    def descrever(self):
        return f"pedido {self._numero}: {self._bebida} no bar"


class Fila:
    """Invocador: guarda as comandas e decide quando executá-las; só conhece Comando."""

    def __init__(self):
        self._pendentes = []
        self.historico = []

    def receber(self, comando):
        self._pendentes.append(comando)

    def pendentes(self):
        return len(self._pendentes)

    def atender_todos(self):
        for comando in self._pendentes:
            comando.executar()
            self.historico.append(comando.descrever())
        self._pendentes.clear()


def main():
    cozinha = Cozinha()
    bar = Bar()
    fila = Fila()

    # Cliente: o caixa cria cada comanda, ligada ao seu receptor, e a entrega à fila
    fila.receber(PrepararLanche(cozinha, 1, "X-burguer"))
    fila.receber(PrepararBebida(bar, 2, "suco de laranja"))
    fila.receber(PrepararLanche(cozinha, 3, "misto quente"))
    print(f"caixa: {fila.pendentes()} pedidos registrados, nenhum preparado ainda")

    # Mais tarde, quando há quem prepare, a fila executa as comandas na ordem
    fila.atender_todos()

    print("historico da fila:")
    for linha in fila.historico:
        print(f"  {linha}")


if __name__ == "__main__":
    main()
