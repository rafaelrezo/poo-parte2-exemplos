from abc import ABC, abstractmethod


class Cozinha:
    """Receptor: sabe preparar e decide se aceita cada pedido."""

    def __init__(self, paes):
        self._paes = paes
        self._preparados = set()

    def preparar(self, numero, item):
        if numero in self._preparados:
            return "repetido, ignorado"
        if self._paes == 0:
            return "recusado, acabou o pao"
        self._paes -= 1
        self._preparados.add(numero)
        return f"pronto ({item})"

    def repor_paes(self, quantidade):
        self._paes += quantidade
        return f"estoque com {self._paes} paes"


class Comando(ABC):
    """Comando: a solicitação como objeto, com uma única operação para executá-la."""

    @abstractmethod
    def descrever(self):
        """Texto curto que identifica a solicitação no histórico."""

    @abstractmethod
    def executar(self):
        """Encaminha a solicitação ao receptor e devolve o resultado."""


class PrepararPedido(Comando):
    def __init__(self, cozinha, numero, item):
        self._cozinha = cozinha
        self._numero = numero
        self._item = item

    def descrever(self):
        return f"pedido {self._numero}"

    def executar(self):
        return self._cozinha.preparar(self._numero, self._item)


class ReporPaes(Comando):
    def __init__(self, cozinha, quantidade):
        self._cozinha = cozinha
        self._quantidade = quantidade

    def descrever(self):
        return f"repor {self._quantidade} paes"

    def executar(self):
        return self._cozinha.repor_paes(self._quantidade)


class Fila:
    """Invocador: guarda as comandas e as executa na ordem, sem conhecer a cozinha."""

    def __init__(self):
        self._pendentes = []
        self.historico = []

    def receber(self, comando):
        self._pendentes.append(comando)

    def pendentes(self):
        return len(self._pendentes)

    def atender_todos(self):
        for comando in self._pendentes:
            self.historico.append(f"{comando.descrever()}: {comando.executar()}")
        self._pendentes.clear()


def main():
    cozinha = Cozinha(2)
    fila = Fila()

    # Clientes: caixa e aplicativo criam comandas e voltam a atender
    fila.receber(PrepararPedido(cozinha, 1, "X-burguer"))
    fila.receber(PrepararPedido(cozinha, 2, "misto quente"))
    fila.receber(PrepararPedido(cozinha, 2, "misto quente"))  # reenvio
    fila.receber(PrepararPedido(cozinha, 3, "X-salada"))
    fila.receber(ReporPaes(cozinha, 10))
    fila.receber(PrepararPedido(cozinha, 4, "X-burguer"))
    print(f"na fila: {fila.pendentes()} comandas, nenhuma executada")

    fila.atender_todos()
    for linha in fila.historico:
        print(linha)


if __name__ == "__main__":
    main()
