from lib.observador import Observador


class Painel(Observador):
    def receber(self, evento):
        print(f"  painel: PRONTO {evento.numero}")


class Aplicativo(Observador):
    def receber(self, evento):
        print(f"  app: pedido {evento.numero} pronto, pode retirar")
