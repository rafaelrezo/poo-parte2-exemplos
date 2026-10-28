class SensorTemperatura:
    def ler(self):
        return 92.5  # valor simulado


class PoliticaAlarme:
    def __init__(self, limite):
        self._limite = limite

    def aciona(self, temperatura):
        return temperatura > self._limite


class RepositorioTemperatura:
    def __init__(self):
        self._registros = []

    def salvar(self, temperatura):
        self._registros.append(temperatura)

    def todos(self):
        return list(self._registros)


class NotificadorEmail:
    def __init__(self, destinatario):
        self._destinatario = destinatario

    def enviar(self, mensagem):
        print(f"[e-mail para {self._destinatario}] {mensagem}")


class MonitorTemperatura:
    """Coordena a sequência: ler, guardar, decidir e avisar."""

    def __init__(self):
        # Ainda cria as próprias peças. Voltaremos a isso na seção 7 (DIP).
        self.sensor = SensorTemperatura()
        self.politica = PoliticaAlarme(limite=90)
        self.repositorio = RepositorioTemperatura()
        self.notificador = NotificadorEmail("operador@planta")

    def verificar(self):
        temperatura = self.sensor.ler()
        self.repositorio.salvar(temperatura)
        if self.politica.aciona(temperatura):
            self.notificador.enviar(f"ALERTA: {temperatura} °C")
        return temperatura


def main():
    monitor = MonitorTemperatura()
    monitor.verificar()
    print(f"registros: {monitor.repositorio.todos()}")


if __name__ == "__main__":
    main()
