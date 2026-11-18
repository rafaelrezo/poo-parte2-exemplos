from lib.contrato import RepositorioPedidos
from lib.modelo import Pedido


class Caixa:
    """Cliente do contrato; não importa os armazenamentos concretos."""

    def __init__(self, pedidos: RepositorioPedidos):
        self._pedidos = pedidos

    def vender(self, item: str, setor: str, valor: float) -> int:
        pedido = Pedido(self._pedidos.ultimo_numero() + 1, item, setor, valor)
        if not self._pedidos.adicionar(pedido):
            raise ValueError("numero de pedido ja registrado")
        print(f"caixa: pedido {pedido.numero} registrado")
        return pedido.numero


class Relatorio:
    """Outro cliente do contrato; não conhece SQL."""

    def __init__(self, pedidos: RepositorioPedidos):
        self._pedidos = pedidos

    def imprimir(self):
        print("faturamento por setor:")
        for setor, total in self._pedidos.faturamento_por_setor().items():
            print(f"  {setor}: R$ {total:.2f}")
