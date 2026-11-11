from observer import Aviso, Cozinha, Fila, Observador, PrepararPedido  # observer.py não é modificado


class Contador(Observador):
    """Observador novo: o gerente quer saber quantos lanches saíram."""

    def __init__(self):
        self.entregues = 0

    def receber(self, aviso):
        if aviso.pronto:
            self.entregues += 1


def testar_contador_isolado():
    # Prepara: o observador sozinho, sem cozinha
    contador = Contador()
    # Executa: entrega avisos fabricados no próprio teste
    contador.receber(Aviso(1, "X-burguer", True))
    contador.receber(Aviso(2, "X-salada", False))
    contador.receber(Aviso(3, "misto quente", True))
    # Confere: só os prontos contam
    assert contador.entregues == 2
    print("teste do contador isolado: ok")


def main():
    testar_contador_isolado()
    contador = Contador()
    cozinha = Cozinha(5)
    cozinha.assinar(contador)  # nenhum painel nem app: só o contador

    fila = Fila()
    fila.receber(PrepararPedido(cozinha, 1, "X-burguer"))
    fila.receber(PrepararPedido(cozinha, 1, "X-burguer"))  # reenvio
    fila.receber(PrepararPedido(cozinha, 2, "misto quente"))
    fila.atender_todos()
    print(f"comandas atendidas: {len(fila.historico)}, lanches entregues: {contador.entregues}")


if __name__ == "__main__":
    main()
