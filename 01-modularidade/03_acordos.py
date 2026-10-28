from dataclasses import dataclass


class PoliticaAlarme:
    def __init__(self, limite, margem):
        self._limite = limite   # nível que aciona
        self._margem = margem   # zona morta

    def aciona(self, nivel):
        return nivel > self._limite


@dataclass(frozen=True)
class LeituraNivelPercentual:
    valor: float


class PoliticaAlarmeSegura:
    def __init__(self, *, limite, margem):  # * exige argumentos nomeados
        self._limite = limite
        self._margem = margem

    def aciona(self, leitura: LeituraNivelPercentual):
        return leitura.valor > self._limite


def main():
    nivel = 30.0  # nivel moderado — não deveria gerar alarme

    correta   = PoliticaAlarme(80, 5)   # intenção: limite=80%, margem=5%
    invertida = PoliticaAlarme(5, 80)   # limite e margem trocados

    print(f"Nivel 30% — correta   (limite=80, margem=5): "
          f"{'ALERTA' if correta.aciona(nivel) else 'NORMAL'}")
    print(f"Nivel 30% — invertida (limite=5, margem=80): "
          f"{'ALERTA' if invertida.aciona(nivel) else 'NORMAL'}")

    # Solução: argumentos nomeados — a ordem deixa de importar
    segura = PoliticaAlarmeSegura(limite=80, margem=5)
    leitura = LeituraNivelPercentual(valor=30)
    print(f"Com argumentos nomeados              : "
          f"{'ALERTA' if segura.aciona(leitura) else 'NORMAL'}")


if __name__ == "__main__":
    main()
