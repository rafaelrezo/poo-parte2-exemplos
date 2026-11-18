import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AquisicaoNivel:
    """Aquisição de nível que já respeitou o contrato."""

    sessao: str
    ciclo: int
    instante: datetime
    nivel: float


def rejeitar_constante(texto: str):
    raise ValueError(f"{texto} não é uma medição")


def validar_envelope(documento) -> tuple:
    """Confere versão, sessão, ciclo e timestamp: a identidade da aquisição."""
    if not isinstance(documento, dict):
        raise ValueError("objeto JSON esperado")
    if type(documento.get("versao")) is not int or documento["versao"] != 1:
        raise ValueError("versão do contrato diferente de 1")
    sessao = documento.get("sessao")
    if not isinstance(sessao, str) or not sessao.strip():
        raise ValueError("sessão ausente")
    ciclo = documento.get("ciclo")
    if type(ciclo) is not int or ciclo <= 0:
        raise ValueError("ciclo deve ser inteiro positivo")
    timestamp = documento.get("timestamp")
    try:
        instante = datetime.strptime(str(timestamp), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("timestamp fora do formato AAAA-MM-DDTHH:MM:SSZ") from None
    return sessao, ciclo, instante.replace(tzinfo=timezone.utc)


def validar_nivel(documento) -> float:
    """Procura a leitura LT-01 e confere tipo, unidade, status e faixa."""
    leituras = documento.get("leituras")
    if not isinstance(leituras, list):
        raise ValueError("lista de leituras ausente")
    for leitura in leituras:
        if isinstance(leitura, dict) and leitura.get("tag") == "LT-01":
            break
    else:
        raise ValueError("leitura LT-01 ausente")
    if leitura.get("tipo") != "nivel" or leitura.get("unidade") != "%":
        raise ValueError(f"LT-01 deve ser nível em %, recebido {leitura.get('unidade')!r}")
    if leitura.get("status") != "operando":
        raise ValueError(f"LT-01 com status {leitura.get('status')!r}")
    valor = leitura.get("valor")
    if type(valor) not in (int, float):
        raise ValueError(f"LT-01: número esperado, recebido {valor!r}")
    if not math.isfinite(valor) or not 0 <= valor <= 100:
        raise ValueError(f"LT-01: {valor} % fora da faixa 0 a 100")
    return float(valor)


def interpretar(texto: str) -> AquisicaoNivel:
    try:
        documento = json.loads(texto, parse_constant=rejeitar_constante)  # 1. parsing
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON ilegível na coluna {erro.colno}") from None
    sessao, ciclo, instante = validar_envelope(documento)                 # 2. validação
    nivel = validar_nivel(documento)
    return AquisicaoNivel(sessao, ciclo, instante, nivel)                 # 3. objeto do domínio
