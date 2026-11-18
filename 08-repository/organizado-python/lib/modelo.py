from dataclasses import dataclass


@dataclass(frozen=True)
class Pedido:
    numero: int
    item: str
    setor: str
    valor: float
