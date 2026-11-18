from lib.modalidades import PorFaixa, PorPeso, Retirada


def criar_frete(nome):
    """Montagem: o único lugar que conhece as modalidades concretas."""
    if nome == "retirada":
        return Retirada()
    if nome == "por_peso":
        return PorPeso()
    if nome == "por_faixa":
        return PorFaixa()
    raise ValueError(f"modalidade de frete desconhecida: {nome}")
