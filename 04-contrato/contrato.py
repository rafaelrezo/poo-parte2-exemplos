import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AquisicaoNivel:
    sessao: str
    ciclo: int
    instante: datetime
    nivel: float


def rejeitar_constante(texto):
    raise ValueError(f"constante JSON invalida: {texto}")


def interpretar(texto):
    doc = json.loads(texto, parse_constant=rejeitar_constante)
    if not isinstance(doc, dict):
        raise ValueError("objeto JSON esperado")
    if type(doc.get("versao")) is not int or doc["versao"] != 1:
        raise ValueError("versao invalida")
    sessao = doc.get("sessao")
    ciclo = doc.get("ciclo")
    if not isinstance(sessao, str) or not sessao.strip():
        raise ValueError("sessao invalida")
    if type(ciclo) is not int or ciclo <= 0:
        raise ValueError("ciclo invalido")
    timestamp = doc.get("timestamp")
    if not isinstance(timestamp, str):
        raise ValueError("timestamp textual esperado")
    instante = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    if instante.strftime("%Y-%m-%dT%H:%M:%SZ") != timestamp:
        raise ValueError("timestamp fora do formato UTC combinado")
    leituras = doc.get("leituras")
    if not isinstance(leituras, list) or len(leituras) != 1:
        raise ValueError("o recorte espera uma leitura")
    leitura = leituras[0]
    if not isinstance(leitura, dict):
        raise ValueError("leitura deve ser um objeto")
    if (leitura.get("tag") != "LT-01" or leitura.get("tipo") != "nivel"
            or leitura.get("unidade") != "%"
            or leitura.get("status") != "operando"):
        raise ValueError("identificacao, unidade ou status invalido")
    valor = leitura.get("valor")
    if type(valor) not in (int, float):
        raise ValueError("numero esperado, sem booleano")
    if not 0 <= valor <= 100 or not math.isfinite(valor):
        raise ValueError("nivel fora da faixa ou nao finito")
    return AquisicaoNivel(sessao, ciclo,
                          instante.replace(tzinfo=timezone.utc), float(valor))


def main():
    documento = {
        "versao": 1, "sessao": "ensaio", "ciclo": 12,
        "timestamp": "2026-10-21T18:00:00Z",
        "leituras": [{"tag": "LT-01", "tipo": "nivel", "valor": 48.5,
                      "unidade": "%", "status": "operando"}],
    }
    ultimo = interpretar(json.dumps(documento, allow_nan=False))
    print(f"VALIDO: {ultimo.sessao}/{ultimo.ciclo} = {ultimo.nivel} %")
    documento["leituras"][0]["valor"] = True
    try:
        interpretar(json.dumps(documento, allow_nan=False))
    except ValueError as erro:
        print(f"REJEITADO: {erro}")
    agora = datetime(2026, 10, 21, 18, 0, 10, tzinfo=timezone.utc)
    idade = (agora - ultimo.instante).total_seconds()
    print(f"ultimo valido: idade={idade:.0f}s; aquisicao atual indisponivel")


if __name__ == "__main__":
    main()
