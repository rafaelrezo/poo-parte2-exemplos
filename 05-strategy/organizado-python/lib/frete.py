from abc import ABC, abstractmethod


class Frete(ABC):
    """Estratégia: o contrato comum a todas as modalidades de frete."""

    @abstractmethod
    def calcular(self, peso_kg):
        """Recebe o peso em kg e devolve o valor do frete em reais."""
