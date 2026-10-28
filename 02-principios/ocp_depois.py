from abc import ABC, abstractmethod


class PoliticaAlarme(ABC):
    @abstractmethod
    def aciona(self, temperatura):
        """Devolve True quando a leitura deve gerar alarme."""


class AlarmeMaximo(PoliticaAlarme):
    def __init__(self, maximo):
        self._maximo = maximo

    def aciona(self, temperatura):
        return temperatura > self._maximo


class AlarmeMinimo(PoliticaAlarme):
    def __init__(self, minimo):
        self._minimo = minimo

    def aciona(self, temperatura):
        return temperatura < self._minimo


class AlarmeFaixa(PoliticaAlarme):
    def __init__(self, minimo, maximo):
        if minimo >= maximo:
            raise ValueError("o mínimo deve ser menor que o máximo")
        self._minimo = minimo
        self._maximo = maximo

    def aciona(self, temperatura):
        return not (self._minimo <= temperatura <= self._maximo)


class AlarmeVariacaoBrusca(PoliticaAlarme):
    """Extensão nova: compara com a leitura anterior. O controlador não muda."""

    def __init__(self, variacao_maxima):
        self._variacao_maxima = variacao_maxima
        self._anterior = None

    def aciona(self, temperatura):
        brusca = (self._anterior is not None
                  and abs(temperatura - self._anterior) > self._variacao_maxima)
        self._anterior = temperatura
        return brusca


class ControladorAlarme:
    def __init__(self, politica):
        self._politica = politica

    def avaliar(self, temperatura):
        return self._politica.aciona(temperatura)


def main():
    politicas = {
        "máximo 90": AlarmeMaximo(90),
        "mínimo 20": AlarmeMinimo(20),
        "faixa 20–90": AlarmeFaixa(20, 90),
        "variação 30": AlarmeVariacaoBrusca(30),
    }
    for nome, politica in politicas.items():
        controlador = ControladorAlarme(politica)
        resultados = [controlador.avaliar(t) for t in (15, 50, 95)]
        print(f"{nome:12} 15 °C, 50 °C, 95 °C -> {resultados}")


if __name__ == "__main__":
    main()
