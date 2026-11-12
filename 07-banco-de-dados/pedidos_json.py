import json
from dataclasses import asdict, dataclass
from pathlib import Path

ARQUIVO = Path("pedidos.json")


@dataclass
class Pedido:
    numero: int
    item: str
    setor: str
    valor: float


def carregar():
    if not ARQUIVO.exists():
        return []
    with ARQUIVO.open(encoding="utf-8") as arquivo:
        return [Pedido(**dados) for dados in json.load(arquivo)]


def gravar(pedidos):
    with ARQUIVO.open("w", encoding="utf-8") as arquivo:
        json.dump([asdict(pedido) for pedido in pedidos], arquivo, ensure_ascii=False, indent=2)


def main():
    pedidos = carregar()
    print(f"pedidos ao abrir o programa: {len(pedidos)}")

    pedidos.append(Pedido(1, "X-burguer", "cozinha", 18.0))
    pedidos.append(Pedido(2, "suco de laranja", "bar", 7.5))
    pedidos.append(Pedido(3, "misto quente", "cozinha", 12.0))
    gravar(pedidos)

    numeros = [pedido.numero for pedido in pedidos]
    print(f"pedidos no arquivo: {len(pedidos)}, numeros {numeros}")


if __name__ == "__main__":
    main()
