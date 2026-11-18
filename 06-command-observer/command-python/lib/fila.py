from lib.comando import Comando


class Fila:
    """Invocador: guarda as comandas e decide quando executá-las; só conhece Comando."""

    def __init__(self):
        self._pendentes = []
        self.historico = []

    def receber(self, comando: Comando):
        self._pendentes.append(comando)

    def pendentes(self):
        return len(self._pendentes)

    def atender_todos(self):
        for comando in self._pendentes:
            comando.executar()
            self.historico.append(comando.descrever())
        self._pendentes.clear()
