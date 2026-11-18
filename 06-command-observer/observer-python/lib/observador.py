from abc import ABC, abstractmethod


class Observador(ABC):
    """Observador: o contrato de quem quer ser avisado."""

    @abstractmethod
    def receber(self, evento):
        """Reage a um evento publicado pela cozinha."""
