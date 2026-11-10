from collections import deque
from enum import Enum
from statistics import median


class ModoFiltro(Enum):
    ULTIMO_VALOR = 1
    MEDIA_MOVEL = 2
    MEDIANA = 3


class CanalNivel:
    def __init__(self, modo, janela):
        if janela < 1:
            raise ValueError("a janela precisa ter ao menos uma leitura")
        self._modo = modo
        self._recentes = deque(maxlen=janela)  # vazia no modo ULTIMO_VALOR

    def receber(self, bruto):
        if not 0.0 <= bruto <= 100.0:
            raise ValueError("nível fora de 0 a 100 %")
        if self._modo == ModoFiltro.ULTIMO_VALOR:
            return bruto
        self._recentes.append(bruto)
        if self._modo == ModoFiltro.MEDIA_MOVEL:
            return sum(self._recentes) / len(self._recentes)
        # ModoFiltro.MEDIANA: acrescentado depois, dentro do mesmo método
        return median(self._recentes)


def main():
    leituras = [48.0, 48.6, 47.8, 48.4, 93.0, 48.2, 47.6, 48.0]

    ultimo = CanalNivel(ModoFiltro.ULTIMO_VALOR, 1)
    media = CanalNivel(ModoFiltro.MEDIA_MOVEL, 3)
    mediana = CanalNivel(ModoFiltro.MEDIANA, 3)

    print("bruto  ultimo  media3  mediana3")
    for bruto in leituras:
        print(f"{bruto:5.1f}  {ultimo.receber(bruto):6.1f}  "
              f"{media.receber(bruto):6.1f}  {mediana.receber(bruto):8.1f}")


if __name__ == "__main__":
    main()
