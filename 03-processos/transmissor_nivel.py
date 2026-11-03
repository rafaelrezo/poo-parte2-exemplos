import sys
from pathlib import Path


class TransmissorNivel:
    """Simula o transmissor: publica o nível em % num arquivo de texto."""

    def __init__(self, caminho: Path):
        self._caminho = caminho

    def publicar(self, nivel: float) -> None:
        texto = f"nivel {nivel}\nunidade %\n"
        self._caminho.write_text(texto, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        print("uso: python3 transmissor_nivel.py NIVEL")
        raise SystemExit(2)
    nivel = float(sys.argv[1])
    TransmissorNivel(Path("nivel.txt")).publicar(nivel)
    print(f"transmissor: nível {nivel} % gravado em nivel.txt")


if __name__ == "__main__":
    main()
