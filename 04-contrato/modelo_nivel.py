import argparse
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from publicar import publicar_atomico


class ModeloNivel:
    """Modelo simples do tanque: a cada ciclo, o nível varia ao acaso até 2 pontos."""

    def __init__(self, nivel_inicial: float, semente: int):
        self._nivel = nivel_inicial
        self._sorteio = random.Random(semente)  # mesma semente, mesma sequência

    def proximo(self) -> float:
        variacao = self._sorteio.uniform(-2.0, 2.0)
        self._nivel = min(100.0, max(0.0, self._nivel + variacao))
        return round(self._nivel, 2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publica aquisições de nível em JSON.")
    parser.add_argument("--ciclos", type=int, default=10)
    parser.add_argument("--intervalo", type=float, default=1.0, help="segundos entre ciclos")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    caminho = Path("aquisicao.json")
    sessao = uuid.uuid4().hex[:8]  # nova a cada execução
    modelo = ModeloNivel(nivel_inicial=50.0, semente=args.seed)

    for ciclo in range(1, args.ciclos + 1):
        nivel = modelo.proximo()
        instante = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        publicar_atomico(caminho, {
            "versao": 1, "sessao": sessao, "ciclo": ciclo, "timestamp": instante,
            "leituras": [{"tag": "LT-01", "tipo": "nivel", "valor": nivel,
                          "unidade": "%", "status": "operando"}],
        })
        print(f"modelo: sessão {sessao} ciclo {ciclo:2} {instante} nível {nivel} %",
              flush=True)
        time.sleep(args.intervalo)


if __name__ == "__main__":
    main()
