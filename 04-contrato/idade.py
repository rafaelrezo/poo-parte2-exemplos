from datetime import datetime, timedelta, timezone

from contrato import AquisicaoNivel


class UltimaAquisicao:
    """Guarda a última aquisição válida e responde se ela ainda é atual."""

    def __init__(self, limite_segundos: float):
        self._limite = timedelta(seconds=limite_segundos)
        self._ultima = None

    def receber(self, aquisicao: AquisicaoNivel) -> str:
        if self._ultima is not None and (aquisicao.sessao, aquisicao.ciclo) == (
                self._ultima.sessao, self._ultima.ciclo):
            return "repetida (mesma sessão e ciclo): nada novo"
        self._ultima = aquisicao
        return "nova"

    def situacao(self, agora: datetime) -> str:
        if self._ultima is None:
            return "sem aquisição válida"
        idade = (agora - self._ultima.instante).total_seconds()
        if idade < 0:
            return "timestamp no futuro: conferir os relógios"
        estado = "OBSOLETA" if idade > self._limite.total_seconds() else "atual"
        return f"{estado}: ciclo {self._ultima.ciclo}, {self._ultima.nivel} %, idade {idade:.0f} s"


def instante(segundo: int) -> datetime:
    return datetime(2026, 10, 21, 18, 0, segundo, tzinfo=timezone.utc)


def main() -> None:
    ultima = UltimaAquisicao(limite_segundos=5)
    ciclo_12 = AquisicaoNivel("ensaio", 12, instante(0), 48.5)
    ciclo_13 = AquisicaoNivel("ensaio", 13, instante(11), 49.1)

    print("18:00:00 recebe ciclo 12 ->", ultima.receber(ciclo_12))
    print("18:00:02 situação        ->", ultima.situacao(instante(2)))
    print("18:00:05 recebe ciclo 12 ->", ultima.receber(ciclo_12))
    print("18:00:10 situação        ->", ultima.situacao(instante(10)))
    print("18:00:11 recebe ciclo 13 ->", ultima.receber(ciclo_13))
    print("18:00:12 situação        ->", ultima.situacao(instante(12)))


if __name__ == "__main__":
    main()
