from dataclasses import dataclass


@dataclass(frozen=True)
class EventoAlarme:
    ativo: bool


class Registro:
    def __init__(self):
        self.mensagens = []

    def receber(self, evento):
        self.mensagens.append("ATIVOU" if evento.ativo else "NORMALIZOU")


class Contador:
    def __init__(self):
        self.quantidade = 0

    def receber(self, evento):
        self.quantidade += 1


class MonitorNivel:
    def __init__(self):
        self._ativo = False
        self._observadores = []

    def assinar(self, observador):
        if not any(atual is observador for atual in self._observadores):
            self._observadores.append(observador)

    def avaliar(self, nivel):
        novo = nivel > 80
        if novo == self._ativo:
            return
        self._ativo = novo
        for observador in self._observadores:
            observador.receber(EventoAlarme(novo))


def main():
    registro = Registro()
    contador = Contador()
    monitor = MonitorNivel()
    monitor.assinar(registro)
    monitor.assinar(contador)
    monitor.assinar(contador)
    for nivel in [79, 81, 82, 80]:
        monitor.avaliar(nivel)
    assert contador.quantidade == 2
    print("\n".join(registro.mensagens))
    print(f"transicoes: {contador.quantidade}")


if __name__ == "__main__":
    main()
