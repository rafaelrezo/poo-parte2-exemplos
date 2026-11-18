from lib.comandos import PrepararBebida, PrepararLanche
from lib.fila import Fila
from lib.receptores import Bar, Cozinha


def main():
    cozinha = Cozinha()
    bar = Bar()
    fila = Fila()

    # Cliente: o caixa cria cada comanda, ligada ao seu receptor, e a entrega à fila
    fila.receber(PrepararLanche(cozinha, 1, "X-burguer"))
    fila.receber(PrepararBebida(bar, 2, "suco de laranja"))
    fila.receber(PrepararLanche(cozinha, 3, "misto quente"))
    print(f"caixa: {fila.pendentes()} pedidos registrados, nenhum preparado ainda")

    # Mais tarde, quando há quem prepare, a fila executa as comandas na ordem
    fila.atender_todos()

    print("historico da fila:")
    for linha in fila.historico:
        print(f"  {linha}")


if __name__ == "__main__":
    main()
