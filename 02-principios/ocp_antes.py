class ControladorAlarme:
    def __init__(self, tipo, minimo=None, maximo=None):
        self._tipo = tipo
        self._minimo = minimo
        self._maximo = maximo

    def avaliar(self, temperatura):
        if self._tipo == "maximo":
            return temperatura > self._maximo
        elif self._tipo == "minimo":
            return temperatura < self._minimo
        elif self._tipo == "faixa":
            return not (self._minimo <= temperatura <= self._maximo)
        raise ValueError(f"tipo de alarme desconhecido: {self._tipo}")


def main():
    controladores = {
        "máximo 90": ControladorAlarme("maximo", maximo=90),
        "mínimo 20": ControladorAlarme("minimo", minimo=20),
        "faixa 20–90": ControladorAlarme("faixa", minimo=20, maximo=90),
    }
    for nome, controlador in controladores.items():
        resultados = [controlador.avaliar(t) for t in (15, 50, 95)]
        print(f"{nome:12} 15 °C, 50 °C, 95 °C -> {resultados}")


if __name__ == "__main__":
    main()
