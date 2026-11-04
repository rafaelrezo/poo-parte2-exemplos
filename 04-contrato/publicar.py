import json
import os
import tempfile
from pathlib import Path

from contrato import interpretar


def publicar_atomico(caminho: Path, documento: dict) -> None:
    """Grava num temporário da mesma pasta e só então substitui o destino."""
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=caminho.parent,
            prefix=f".{caminho.name}.", suffix=".tmp", delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(documento, arquivo, allow_nan=False)
        os.replace(temporario, caminho)  # troca o arquivo inteiro de uma vez
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def aquisicao(ciclo: int, nivel: float) -> dict:
    return {"versao": 1, "sessao": "ensaio", "ciclo": ciclo,
            "timestamp": f"2026-10-21T18:00:{ciclo:02d}Z",
            "leituras": [{"tag": "LT-01", "tipo": "nivel", "valor": nivel,
                          "unidade": "%", "status": "operando"}]}


def ler(caminho: Path) -> None:
    try:
        lida = interpretar(caminho.read_text(encoding="utf-8"))
        print(f"  leitor: ciclo {lida.ciclo}, {lida.nivel} %")
    except ValueError as erro:
        print(f"  leitor: RECUSADO ({erro})")


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "planta.json"

        print("1) escritor publica o ciclo 12 de forma atômica")
        publicar_atomico(caminho, aquisicao(12, 48.5))
        ler(caminho)

        print("2) sem a técnica: o escritor grava direto no destino e é interrompido")
        texto = json.dumps(aquisicao(13, 49.1))
        caminho.write_text(texto[: len(texto) // 2], encoding="utf-8")
        ler(caminho)

        print("3) escritor publica o ciclo 14 de forma atômica")
        publicar_atomico(caminho, aquisicao(14, 49.6))
        ler(caminho)
        print("  arquivos na pasta:", sorted(p.name for p in Path(pasta).iterdir()))


if __name__ == "__main__":
    main()
