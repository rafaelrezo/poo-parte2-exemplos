import json


def nivel_alto(texto: str) -> bool:
    """Versão ingênua: abre o JSON e usa o valor sem conferir nada."""
    documento = json.loads(texto)
    valor = documento["leituras"][0]["valor"]
    return valor > 80


def main() -> None:
    casos = [(48.5, "%"), (95.0, "%"), (True, "%"), (0.95, "fracao"), ("alto", "%")]
    for valor, unidade in casos:
        leitura = {"tag": "LT-01", "valor": valor, "unidade": unidade}
        texto = json.dumps({"leituras": [leitura]})
        try:
            print(f"valor={valor!r:7} unidade={unidade:7} -> nível alto? {nivel_alto(texto)}")
        except TypeError as erro:
            print(f"valor={valor!r:7} unidade={unidade:7} -> TypeError: {erro}")


if __name__ == "__main__":
    main()
