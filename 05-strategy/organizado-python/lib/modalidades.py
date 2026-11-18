from lib.frete import Frete


class Retirada(Frete):
    def calcular(self, peso_kg):
        return 0.0


class PorPeso(Frete):
    def calcular(self, peso_kg):
        return 8.0 + 4.0 * peso_kg


class PorFaixa(Frete):
    def calcular(self, peso_kg):
        if peso_kg <= 1.0:
            return 15.0
        if peso_kg <= 5.0:
            return 25.0
        return 35.0
