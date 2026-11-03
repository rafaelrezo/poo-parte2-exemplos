from pathlib import Path


def ler_campos(caminho: Path) -> dict:
    """Lê linhas no formato 'chave valor'."""
    campos = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        chave, valor = linha.split(maxsplit=1)
        campos[chave] = valor
    return campos


class PainelBomba:
    """Simula o painel elétrico: só liga o motor se o nível permitir."""

    def __init__(self, nivel_minimo: float):
        self._nivel_minimo = nivel_minimo

    def atender(self, nivel: float) -> tuple:
        if nivel < self._nivel_minimo:
            return "desligada", "nivel_baixo"
        return "ligada", "ok"


def main() -> None:
    pedido = ler_campos(Path("comando.txt"))
    nivel = float(ler_campos(Path("nivel.txt"))["nivel"])
    estado, motivo = PainelBomba(nivel_minimo=10.0).atender(nivel)
    resposta = f"ultimo_comando {pedido['id']}\nbomba {estado}\nmotivo {motivo}\n"
    Path("estado_bomba.txt").write_text(resposta, encoding="utf-8")
    print(f"painel: pedido {pedido['id']} atendido -> bomba {estado} ({motivo})")


if __name__ == "__main__":
    main()
