from abc import ABC, abstractmethod
from collections import deque
from statistics import median


class FiltroSinal(ABC):
    """Estratégia: o contrato comum a todos os filtros."""

    @abstractmethod
    def filtrar(self, bruto):
        """Recebe uma leitura válida em % e devolve o valor tratado."""


class UltimoValor(FiltroSinal):
    def filtrar(self, bruto):
        return bruto


class MediaMovel(FiltroSinal):
    def __init__(self, janela):
        if janela < 1:
            raise ValueError("a janela precisa ter ao menos uma leitura")
        self._recentes = deque(maxlen=janela)

    def filtrar(self, bruto):
        self._recentes.append(bruto)
        return sum(self._recentes) / len(self._recentes)


class Mediana(FiltroSinal):
    def __init__(self, janela):
        if janela < 1:
            raise ValueError("a janela precisa ter ao menos uma leitura")
        self._recentes = deque(maxlen=janela)

    def filtrar(self, bruto):
        self._recentes.append(bruto)
        return median(self._recentes)


class CanalNivel:
    """Contexto: valida a leitura e delega o tratamento do sinal."""

    def __init__(self, filtro):
        if filtro is None:
            raise ValueError("o canal precisa de um filtro")
        self._filtro = filtro

    def receber(self, bruto):
        if not 0.0 <= bruto <= 100.0:
            raise ValueError("nível fora de 0 a 100 %")
        return self._filtro.filtrar(bruto)


def criar_filtro(nome):
    """Montagem: o único lugar que conhece os filtros concretos."""
    if nome == "ultimo":
        return UltimoValor()
    if nome == "media3":
        return MediaMovel(3)
    if nome == "mediana3":
        return Mediana(3)
    raise ValueError(f"filtro desconhecido: {nome}")


def main():
    leituras = [48.0, 48.6, 47.8, 48.4, 93.0, 48.2, 47.6, 48.0]

    ultimo = CanalNivel(criar_filtro("ultimo"))
    media = CanalNivel(criar_filtro("media3"))
    mediana = CanalNivel(criar_filtro("mediana3"))

    print("bruto  ultimo  media3  mediana3")
    for bruto in leituras:
        print(f"{bruto:5.1f}  {ultimo.receber(bruto):6.1f}  "
              f"{media.receber(bruto):6.1f}  {mediana.receber(bruto):8.1f}")


if __name__ == "__main__":
    main()
