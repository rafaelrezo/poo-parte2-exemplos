from strategy import CanalNivel, FiltroSinal  # strategy.py não é modificado


class MediaExponencial(FiltroSinal):
    """Filtro novo: cada leitura pesa ``alfa``; o histórico pesa ``1 - alfa``."""

    def __init__(self, alfa):
        if not 0.0 < alfa <= 1.0:
            raise ValueError("alfa precisa estar em (0, 1]")
        self._alfa = alfa
        self._anterior = None

    def filtrar(self, bruto):
        if self._anterior is None:
            self._anterior = bruto
        else:
            self._anterior = self._alfa * bruto + (1 - self._alfa) * self._anterior
        return self._anterior


def testar_filtro_isolado():
    # Prepara: o filtro sozinho, sem canal e sem arquivo
    filtro = MediaExponencial(0.5)
    # Executa e confere: 40 -> 40; depois 0,5*60 + 0,5*40 = 50; depois 0,5*60 + 0,5*50 = 55
    assert filtro.filtrar(40.0) == 40.0
    assert filtro.filtrar(60.0) == 50.0
    assert filtro.filtrar(60.0) == 55.0
    print("teste do filtro isolado: ok")


def main():
    testar_filtro_isolado()
    canal = CanalNivel(MediaExponencial(0.5))  # o mesmo CanalNivel de antes
    leituras = [48.0, 48.6, 47.8, 48.4, 93.0, 48.2, 47.6, 48.0]
    tratadas = [f"{canal.receber(bruto):.1f}" for bruto in leituras]
    print("exp0.5:", " ".join(tratadas))


if __name__ == "__main__":
    main()
