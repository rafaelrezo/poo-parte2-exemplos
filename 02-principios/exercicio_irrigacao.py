class SistemaIrrigacao:
    def __init__(self):
        self.registros = []

    def ler_umidade(self):
        return 28.0  # % de umidade do solo, valor simulado

    def executar(self, modo):
        umidade = self.ler_umidade()

        if modo == "economico":
            irrigar = umidade < 25
        elif modo == "normal":
            irrigar = umidade < 35
        else:
            raise ValueError(f"modo desconhecido: {modo}")

        if irrigar:
            print("[válvula V1] aberta por 10 min")
            print(f"[SMS para plantão] irrigação iniciada, umidade {umidade}%")
        else:
            print("[válvula V1] permanece fechada")

        self.registros.append(f"{modo};{umidade};{irrigar}")


def main():
    sistema = SistemaIrrigacao()
    sistema.executar("economico")
    sistema.executar("normal")
    print(f"registros: {sistema.registros}")


if __name__ == "__main__":
    main()
