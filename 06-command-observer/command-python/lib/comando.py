from abc import ABC, abstractmethod


class Comando(ABC):
    """Comando: o contrato comum de toda solicitação."""

    @abstractmethod
    def executar(self):
        """Encaminha a solicitação ao seu receptor."""

    @abstractmethod
    def descrever(self):
        """Texto curto que identifica a solicitação no histórico."""
