import time
from pathlib import Path

from serie import carregar_serie


def main() -> None:
    """Lê serie_nivel.json sem parar durante 3 s e conta as leituras recusadas."""
    validas = 0
    recusadas = 0
    ultimo_erro = ""
    fim = time.monotonic() + 3.0  # relógio monotônico: mede duração
    while time.monotonic() < fim:
        try:
            carregar_serie(Path("serie_nivel.json"))
            validas += 1
        except (OSError, ValueError) as erro:
            recusadas += 1
            ultimo_erro = str(erro)
    print(f"leituras válidas: {validas}, recusadas: {recusadas}")
    if ultimo_erro:
        print(f"último erro: {ultimo_erro}")


if __name__ == "__main__":
    main()
