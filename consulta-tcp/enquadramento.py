import json


class Enquadrador:
    def __init__(self, limite=256):
        self._pendente = b""
        self._limite = limite

    def receber(self, trecho):
        self._pendente += trecho
        mensagens = []
        while b"\n" in self._pendente:
            linha, self._pendente = self._pendente.split(b"\n", 1)
            if len(linha) > self._limite:
                raise ValueError("mensagem excedeu o limite")
            mensagens.append(json.loads(linha.decode("utf-8")))
        if len(self._pendente) > self._limite:
            raise ValueError("mensagem excedeu o limite")
        return mensagens

    def encerrar(self):
        if self._pendente:
            raise ValueError("conexao terminou com mensagem incompleta")


def main():
    receptor = Enquadrador()
    mensagens = receptor.receber(b'{"ciclo":1}\n{"ci')
    mensagens += receptor.receber(b'clo":2}\n')
    receptor.encerrar()
    assert mensagens == [{"ciclo": 1}, {"ciclo": 2}]
    print("ciclos recebidos:", [item["ciclo"] for item in mensagens])
    incompleto = Enquadrador()
    incompleto.receber(b'{"ciclo":')
    try:
        incompleto.encerrar()
    except ValueError as erro:
        print("REJEITADO:", erro)


if __name__ == "__main__":
    main()
