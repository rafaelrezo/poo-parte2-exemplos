import sqlite3
from contextlib import closing

from repositorio import Caixa, Pedido, RepositorioMemoria, RepositorioSQLite  # repositorio.py não é modificado


def verificar_contrato(pedidos):
    """O mesmo teste vale para qualquer implementação do contrato."""
    assert pedidos.ultimo_numero() == 0
    assert pedidos.buscar(1) is None

    lanche = Pedido(1, "X-burguer", "cozinha", 18.0)
    assert pedidos.adicionar(lanche) is True
    assert pedidos.adicionar(lanche) is False  # repetir não duplica
    assert pedidos.adicionar(Pedido(2, "suco de laranja", "bar", 7.5)) is True

    assert pedidos.buscar(1) == lanche
    assert pedidos.ultimo_numero() == 2
    assert pedidos.faturamento_por_setor() == {"bar": 7.5, "cozinha": 18.0}
    print(f"contrato ok: {type(pedidos).__name__}")


def testar_caixa_sem_banco():
    # Prepara: um repositório em memória que já tem o pedido 41
    pedidos = RepositorioMemoria()
    pedidos.adicionar(Pedido(41, "pastel", "cozinha", 9.0))
    # Executa: a regra do caixa, sem SQL e sem arquivo
    numero = Caixa(pedidos).vender("X-burguer", "cozinha", 18.0)
    # Confere: a numeração continua do último pedido guardado
    assert numero == 42
    assert pedidos.buscar(42).item == "X-burguer"
    print("caixa continua a numeracao, testado sem banco: ok")


def main():
    verificar_contrato(RepositorioMemoria())
    with closing(sqlite3.connect(":memory:")) as conexao:
        verificar_contrato(RepositorioSQLite(conexao))
    testar_caixa_sem_banco()


if __name__ == "__main__":
    main()
