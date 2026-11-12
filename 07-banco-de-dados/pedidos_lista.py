from dataclasses import dataclass


@dataclass
class Pedido:
    numero: int
    item: str
    setor: str
    valor: float


def buscar(pedidos, numero):
    for pedido in pedidos:
        if pedido.numero == numero:
            return pedido
    return None


def faturamento_por_setor(pedidos):
    totais = {}
    for pedido in pedidos:
        totais[pedido.setor] = totais.get(pedido.setor, 0) + pedido.valor
    return totais


def main():
    pedidos = []
    print(f"pedidos ao abrir o programa: {len(pedidos)}")

    pedidos.append(Pedido(1, "X-burguer", "cozinha", 18.0))
    pedidos.append(Pedido(2, "suco de laranja", "bar", 7.5))
    pedidos.append(Pedido(3, "misto quente", "cozinha", 12.0))

    print(f"pedidos registrados: {len(pedidos)}")
    print(f"pedido 2: {buscar(pedidos, 2)}")
    print(f"faturamento por setor: {faturamento_por_setor(pedidos)}")


if __name__ == "__main__":
    main()
