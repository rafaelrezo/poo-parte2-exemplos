from abc import ABC, abstractmethod
from typing import Dict, Optional


# ---------- Núcleo: regra, portas e caso de uso. Nenhuma E/S aqui. ----------

class Tarifa(ABC):
    """Regra do negócio; varia por Strategy (aula 05)."""

    @abstractmethod
    def calcular(self, minutos: int) -> int:
        """Valor em centavos para a permanência."""


class TarifaPorHora(Tarifa):
    """15 min grátis; R$ 8,00 por hora iniciada."""

    def calcular(self, minutos: int) -> int:
        if minutos <= 15:
            return 0
        return ((minutos + 59) // 60) * 800


class Relogio(ABC):
    """Porta de saída: o núcleo precisa saber a hora."""

    @abstractmethod
    def agora_em_minutos(self) -> int:
        """Instante atual em minutos."""


class RepositorioEntradas(ABC):
    """Porta de saída: o núcleo precisa lembrar entradas."""

    @abstractmethod
    def guardar(self, placa: str, minuto: int) -> None:
        """Registra o minuto de entrada da placa."""

    @abstractmethod
    def retirar(self, placa: str) -> Optional[int]:
        """Remove e devolve o minuto de entrada, ou None se não houver."""


class ServicoEstacionamento:
    """Porta de entrada: suas operações são os casos de uso."""

    def __init__(self, tarifa: Tarifa, entradas: RepositorioEntradas, relogio: Relogio):
        self._tarifa = tarifa
        self._entradas = entradas
        self._relogio = relogio

    def registrar_entrada(self, placa: str) -> None:
        self._entradas.guardar(placa, self._relogio.agora_em_minutos())

    def registrar_saida(self, placa: str) -> int:
        entrada = self._entradas.retirar(placa)
        if entrada is None:
            raise ValueError(f"não há entrada aberta para {placa}")
        return self._tarifa.calcular(self._relogio.agora_em_minutos() - entrada)


# ---------- Adaptadores de saída: implementam as portas com uma tecnologia ----------

class RelogioSimulado(Relogio):
    def __init__(self, inicio: int):
        self._agora = inicio

    def agora_em_minutos(self) -> int:
        return self._agora

    def avancar(self, minutos: int) -> None:
        self._agora += minutos


class EntradasEmMemoria(RepositorioEntradas):
    def __init__(self):
        self._entradas: Dict[str, int] = {}

    def guardar(self, placa: str, minuto: int) -> None:
        self._entradas[placa] = minuto

    def retirar(self, placa: str) -> Optional[int]:
        return self._entradas.pop(placa, None)


# ---------- Montagem e adaptador de entrada: o único trecho que conhece tudo ----------

def main() -> None:
    relogio = RelogioSimulado(8 * 60)  # 08:00
    servico = ServicoEstacionamento(TarifaPorHora(), EntradasEmMemoria(), relogio)

    servico.registrar_entrada("ABC1D23")
    servico.registrar_entrada("XYZ9876")
    relogio.avancar(10)
    print(f"XYZ9876 pagou {servico.registrar_saida('XYZ9876')} centavos")
    relogio.avancar(85)
    print(f"ABC1D23 pagou {servico.registrar_saida('ABC1D23')} centavos")
    try:
        servico.registrar_saida("ABC1D23")
    except ValueError as erro:
        print(f"erro: {erro}")


if __name__ == "__main__":
    main()
