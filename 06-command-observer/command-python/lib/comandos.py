from lib.comando import Comando


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
