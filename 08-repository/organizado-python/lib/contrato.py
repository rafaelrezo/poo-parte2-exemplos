from abc import ABC, abstractmethod

from lib.modelo import Pedido


class RepositorioPedidos(ABC):
    """Contrato que os clientes conhecem; não escolhe banco nem memória."""

    @abstractmethod
    def adicionar(self, pedido: Pedido) -> bool:
        """Devolve False se o número já existia."""

    @abstractmethod
    def buscar(self, numero: int) -> Pedido | None:
        """Devolve o pedido ou None."""

    @abstractmethod
    def ultimo_numero(self) -> int:
        """Devolve o maior número ou zero."""

    @abstractmethod
    def faturamento_por_setor(self) -> dict[str, float]:
        """Devolve os totais agrupados por setor."""
