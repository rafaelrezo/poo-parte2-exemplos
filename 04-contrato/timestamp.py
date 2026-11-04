import time
from datetime import datetime, timedelta, timezone

FORMATO = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601 em UTC, como no contrato


def para_texto(instante: datetime) -> str:
    return instante.astimezone(timezone.utc).strftime(FORMATO)


def de_texto(texto: str) -> datetime:
    return datetime.strptime(texto, FORMATO).replace(tzinfo=timezone.utc)


def main() -> None:
    # 1. O instante de agora, pelo relógio de parede (muda a cada execução)
    agora = datetime.now(timezone.utc)
    print("agora, em UTC:          ", para_texto(agora))

    # 2. Um mesmo instante, três representações
    ocorrencia = de_texto("2026-10-21T18:00:00Z")
    brasilia = timezone(timedelta(hours=-3))  # Brasília, sem horário de verão
    print("ocorrência em UTC:      ", para_texto(ocorrencia))
    print("a mesma, em Brasília:   ", ocorrencia.astimezone(brasilia).isoformat())
    print("a mesma, em segundos:   ", int(ocorrencia.timestamp()), "(desde 1970-01-01 UTC)")

    # 3. Ocorrência e recebimento são instantes diferentes
    recebimento = de_texto("2026-10-21T18:00:03Z")
    atraso = (recebimento - ocorrencia).total_seconds()
    print("recebida às", para_texto(recebimento), f"-> atraso de {atraso:.0f} s")

    # 4. Em UTC e neste formato, ordem alfabética = ordem no tempo
    eventos = ["2026-10-21T18:00:10Z", "2026-10-21T17:59:58Z", "2026-10-21T18:00:02Z"]
    print("eventos em ordem:       ", sorted(eventos))

    # 5. Duração dentro do programa: relógio monotônico
    inicio = time.monotonic()
    time.sleep(0.2)
    print(f"duração medida:          {time.monotonic() - inicio:.1f} s")


if __name__ == "__main__":
    main()
