from dataclasses import dataclass


@dataclass(frozen=True)
class Registro:
    id: int
    nivel: float


class LivroAuditoria:
    def __init__(self):
        self._registros = {}

    def registrar(self, registro):
        if registro.id <= 0:
            raise ValueError("id deve ser positivo")
        anterior = self._registros.get(registro.id)
        if anterior is not None:
            if anterior != registro:
                raise ValueError("id repetido com outro conteudo")
            return False
        self._registros[registro.id] = registro
        return True

    def quantidade(self):
        return len(self._registros)


class RegistrarNivel:
    def __init__(self, registro):
        self._registro = registro

    def executar(self, receptor):
        return receptor.registrar(self._registro)


class Executor:
    def executar(self, comando, receptor):
        return comando.executar(receptor)


def main():
    livro = LivroAuditoria()
    comando = RegistrarNivel(Registro(7, 48.5))
    executor = Executor()
    primeiro = executor.executar(comando, livro)
    repetido = executor.executar(comando, livro)
    assert primeiro
    assert not repetido
    assert livro.quantidade() == 1
    print(f"registros apos repetir: {livro.quantidade()}")


if __name__ == "__main__":
    main()
