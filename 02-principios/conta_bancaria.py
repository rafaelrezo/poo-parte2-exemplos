class ContaBancaria:
    def __init__(self, titular):
        self._titular = titular
        self._saldo = 0.0
        self._movimentos = []

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("depósito deve ser positivo")
        self._saldo += valor
        self._movimentos.append(("depósito", valor))

    def sacar(self, valor):
        if valor <= 0 or valor > self._saldo:
            raise ValueError("saque inválido")
        self._saldo -= valor
        self._movimentos.append(("saque", valor))

    def saldo(self):
        return self._saldo

    def extrato(self):
        return list(self._movimentos)


def main():
    conta = ContaBancaria("Ana")
    conta.depositar(500)
    conta.sacar(120)
    print(f"saldo: {conta.saldo():.2f}")
    print(f"extrato: {conta.extrato()}")


if __name__ == "__main__":
    main()
