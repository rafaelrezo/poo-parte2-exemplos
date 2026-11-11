from observer import Cozinha, Observador, Painel, PedidoPronto  # observer.py não é modificado


class Contador(Observador):
    """Observador novo: o gerente quer saber quantos pedidos ficaram prontos."""

    def __init__(self):
        self.prontos = 0

    def receber(self, evento):
        self.prontos += 1


def testar_contador_isolado():
    # Prepara: o observador sozinho, sem cozinha
    contador = Contador()
    # Executa: entrega eventos criados no próprio teste
    contador.receber(PedidoPronto(1))
    contador.receber(PedidoPronto(2))
    # Confere: um a mais por evento recebido
    assert contador.prontos == 2
    print("teste do contador isolado: ok")


def main():
    testar_contador_isolado()
    painel = Painel()
    contador = Contador()
    cozinha = Cozinha()  # a mesma Cozinha de antes
    cozinha.assinar(painel)
    cozinha.assinar(contador)  # uma inscrição a mais; nenhuma linha da cozinha mudou

    cozinha.concluir(1)
    cozinha.concluir(2)
    cozinha.concluir(2)  # botão apertado de novo
    print(f"contador do gerente: {contador.prontos} pedidos prontos")


if __name__ == "__main__":
    main()
