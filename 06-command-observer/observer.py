from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Aviso:
    """Evento: o que mudou num pedido."""

    numero: int
    item: str
    pronto: bool  # False: recusado


class Observador(ABC):
    """Contrato de quem quer ser avisado."""

    @abstractmethod
    def receber(self, aviso):
        """Reage a um aviso publicado pela cozinha."""


class Cozinha:
    """Sujeito (e receptor dos comandos): avisa a todos os inscritos, sem conhecê-los."""

    def __init__(self, paes):
        self._paes = paes
        self._preparados = set()
        self._observadores = []

    def assinar(self, observador):
        self._observadores.append(observador)

    def preparar(self, numero, item):
        if numero in self._preparados:
            return "repetido, ignorado"  # nada mudou: ninguém é avisado
        if self._paes == 0:
            self._notificar(Aviso(numero, item, False))
            return "recusado, acabou o pao"
        self._paes -= 1
        self._preparados.add(numero)
        self._notificar(Aviso(numero, item, True))
        return f"pronto ({item})"

    def repor_paes(self, quantidade):
        self._paes += quantidade
        return f"estoque com {self._paes} paes"

    def _notificar(self, aviso):
        for observador in self._observadores:
            observador.receber(aviso)


class Painel(Observador):
    def __init__(self):
        self.prontos = []  # estado: o que está pronto agora

    def receber(self, aviso):
        if aviso.pronto:
            self.prontos.append(aviso.numero)
            print(f"painel: PRONTO {aviso.numero}")


class Aplicativo(Observador):
    def receber(self, aviso):
        if aviso.pronto:
            print(f"app: pedido {aviso.numero} pronto, pode retirar")
        else:
            print(f"app: pedido {aviso.numero} recusado, procure o caixa")


# Comando, comandos concretos e invocador: iguais aos de command.py
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
    painel = Painel()
    app = Aplicativo()
    cozinha = Cozinha(2)
    cozinha.assinar(painel)
    cozinha.assinar(app)

    fila = Fila()
    fila.receber(PrepararPedido(cozinha, 1, "X-burguer"))
    fila.receber(PrepararPedido(cozinha, 2, "misto quente"))
    fila.receber(PrepararPedido(cozinha, 2, "misto quente"))  # reenvio
    fila.receber(PrepararPedido(cozinha, 3, "X-salada"))
    fila.receber(ReporPaes(cozinha, 10))
    fila.receber(PrepararPedido(cozinha, 4, "X-burguer"))

    fila.atender_todos()
    print(f"historico da fila: {len(fila.historico)} comandas")
    print("painel mostra:", *painel.prontos)


if __name__ == "__main__":
    main()
