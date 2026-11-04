import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

FORMATO_TIMESTAMP = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601 em UTC, igual ao C++


@dataclass(frozen=True)
class Medicao:
    ciclo: int
    instante: datetime
    valor: float


def validar_medicao(item, posicao: int) -> Medicao:
    """Confere uma medição da lista e a converte em objeto Python."""
    if not isinstance(item, dict):
        raise ValueError(f"medição {posicao}: objeto JSON esperado")
    ciclo = item.get("ciclo")
    if type(ciclo) is not int or ciclo <= 0:
        raise ValueError(f"medição {posicao}: ciclo deve ser inteiro positivo")
    try:
        instante = datetime.strptime(str(item.get("timestamp")), FORMATO_TIMESTAMP)
    except ValueError:
        raise ValueError(f"medição {posicao}: timestamp fora do formato ISO 8601 UTC") from None
    valor = item.get("valor")
    if type(valor) not in (int, float) or not math.isfinite(valor):
        raise ValueError(f"medição {posicao}: valor deve ser número, recebido {valor!r}")
    if not 0 <= valor <= 100:
        raise ValueError(f"medição {posicao}: {valor} % fora da faixa de 0 a 100")
    return Medicao(ciclo, instante.replace(tzinfo=timezone.utc), float(valor))


def carregar_serie(caminho: Path) -> list:
    """Lê o arquivo, faz o parsing e valida cada medição."""
    texto = caminho.read_text(encoding="utf-8")
    try:
        documento = json.loads(texto)  # parsing: texto -> dict
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON ilegível na linha {erro.lineno}, coluna {erro.colno}") from None
    if not isinstance(documento, dict) or documento.get("unidade") != "%":
        raise ValueError("documento deve ser um objeto com unidade '%'")
    medicoes = documento.get("medicoes")
    if not isinstance(medicoes, list):
        raise ValueError("campo 'medicoes' deve ser uma lista")
    return [validar_medicao(item, posicao) for posicao, item in enumerate(medicoes, start=1)]


def main() -> None:
    try:
        serie = carregar_serie(Path("serie_nivel.json"))
    except (OSError, ValueError) as erro:
        print(f"série recusada: {erro}")
        raise SystemExit(1)
    print(f"{len(serie)} medições válidas")
    print("ciclo  hora (UTC)  nível")
    for medicao in serie:
        print(f"{medicao.ciclo:5}  {medicao.instante:%H:%M:%S}    {medicao.valor:6.2f} %")


if __name__ == "__main__":
    main()
