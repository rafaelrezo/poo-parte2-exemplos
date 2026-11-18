from dataclasses import dataclass


@dataclass(frozen=True)
class PedidoPronto:
    """Evento: o que aconteceu, com os dados que os interessados precisam."""

    numero: int
