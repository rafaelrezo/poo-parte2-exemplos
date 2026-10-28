from abc import ABC, abstractmethod


class ErroArmazenamento(Exception):
    """Falha de gravação prevista no contrato."""


class RepositorioMedicoes(ABC):
    """Contrato:
    - salvar(valor): depois da chamada, ultima() devolve exatamente o valor salvo;
    - falha: se não conseguir gravar, lança ErroArmazenamento e não altera nada.
    """

    @abstractmethod
    def salvar(self, valor):
        """Grava uma medição em °C."""

    @abstractmethod
    def ultima(self):
        """Devolve a última medição gravada."""


class RepositorioMemoria(RepositorioMedicoes):
    def __init__(self):
        self._valores = []

    def salvar(self, valor):
        self._valores.append(valor)

    def ultima(self):
        return self._valores[-1]


class RepositorioDiscoCheio(RepositorioMedicoes):
    def salvar(self, valor):
        raise ErroArmazenamento("disco cheio")  # falha prevista: válido

    def ultima(self):
        raise ErroArmazenamento("nada gravado")


class RepositorioCSVInteiro(RepositorioMedicoes):
    """Grava as linhas de um CSV com formato inteiro, perdendo as casas decimais."""

    def __init__(self):
        self._linhas = []

    def salvar(self, valor):
        self._linhas.append(f"{valor:.0f}")  # 90.4 vira "90": viola a pós-condição

    def ultima(self):
        return float(self._linhas[-1])


def registrar_e_conferir(repositorio, temperatura, limite=90):
    try:
        repositorio.salvar(temperatura)
    except ErroArmazenamento as erro:
        return f"não gravou ({erro})"
    lida = repositorio.ultima()
    situacao = "ALARME" if lida > limite else "normal"
    return f"gravou {temperatura}, leu {lida} -> {situacao}"


def main():
    for repositorio in (RepositorioMemoria(), RepositorioDiscoCheio(), RepositorioCSVInteiro()):
        print(f"{type(repositorio).__name__:21} {registrar_e_conferir(repositorio, 90.4)}")


if __name__ == "__main__":
    main()
