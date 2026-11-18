from lib.contrato import RepositorioPedidos
from lib.modelo import Pedido


class RepositorioMemoria(RepositorioPedidos):
    """Implementação concreta sem arquivo."""

    def __init__(self):
        self._pedidos = {}

    def adicionar(self, pedido: Pedido) -> bool:
        if pedido.numero in self._pedidos:
            return False
        self._pedidos[pedido.numero] = pedido
        return True

    def buscar(self, numero: int) -> Pedido | None:
        return self._pedidos.get(numero)

    def ultimo_numero(self) -> int:
        return max(self._pedidos, default=0)

    def faturamento_por_setor(self) -> dict[str, float]:
        totais = {}
        for pedido in self._pedidos.values():
            totais[pedido.setor] = totais.get(pedido.setor, 0) + pedido.valor
        return dict(sorted(totais.items()))
