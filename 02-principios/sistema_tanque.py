class SistemaTanque:
    def __init__(self):
        self.historico = []

    def ler_temperatura(self):
        return 92.5  # leitura simulada do sensor

    def executar_ciclo(self):
        temperatura = self.ler_temperatura()
        if temperatura > 90:
            bomba = "ligada"
            print(f"[e-mail para operador@planta] ALERTA: {temperatura} °C")
        else:
            bomba = "desligada"
        self.historico.append(f"{temperatura};{bomba}")
        print(f"temperatura {temperatura} °C, bomba de resfriamento {bomba}")


def main():
    sistema = SistemaTanque()
    sistema.executar_ciclo()
    print(f"histórico: {sistema.historico}")


if __name__ == "__main__":
    main()
