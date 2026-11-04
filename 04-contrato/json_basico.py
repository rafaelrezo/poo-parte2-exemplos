import json


def main() -> None:
    leitura = {"tag": "LT-01", "tipo": "nivel", "valor": 48.5,
               "unidade": "%", "status": "operando", "falha": None}

    texto = json.dumps(leitura)  # serializar: dict -> texto
    print("texto JSON:", texto)

    lida = json.loads(texto)  # parsing: texto -> dict
    print("tipo do documento:", type(lida).__name__)
    print("valor:", lida["valor"], "->", type(lida["valor"]).__name__)
    print("falha:", lida["falha"], "->", type(lida["falha"]).__name__)

    try:
        json.loads('{"tag": "LT-01", "valor": 48.5')  # falta fechar a chave
    except json.JSONDecodeError as erro:
        print("texto incompleto:", erro.msg)


if __name__ == "__main__":
    main()
