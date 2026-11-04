from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

from contrato import interpretar

CAMINHO = Path("aquisicao.json")
LIMITE_OBSOLESCENCIA_S = 5.0
BRASILIA = timezone(timedelta(hours=-3))  # conversão só para exibir


def registrar(historico: list, aquisicao) -> None:
    """Guarda a aquisição no histórico da tela só se ela for nova."""
    if historico:
        ultima = historico[-1]
        if (ultima["sessao"], ultima["ciclo"]) == (aquisicao.sessao, aquisicao.ciclo):
            return  # mesmo snapshot lido de novo
        if ultima["sessao"] != aquisicao.sessao:
            historico.clear()  # o dispositivo reiniciou: começa outro gráfico
    historico.append({"sessao": aquisicao.sessao, "ciclo": aquisicao.ciclo,
                      "instante": aquisicao.instante, "nivel": aquisicao.nivel})


@st.fragment(run_every=1.0)  # reexecuta esta função a cada segundo
def painel() -> None:
    historico = st.session_state.setdefault("historico", [])
    try:
        registrar(historico, interpretar(CAMINHO.read_text(encoding="utf-8")))
    except FileNotFoundError:
        st.info(f"Aguardando {CAMINHO}: inicie o dispositivo.")
    except ValueError as erro:
        st.error(f"Aquisição recusada: {erro}")  # o histórico anterior continua
    if not historico:
        return

    ultima = historico[-1]
    idade = (datetime.now(timezone.utc) - ultima["instante"]).total_seconds()
    coluna_nivel, coluna_idade = st.columns(2)
    coluna_nivel.metric("Nível LT-01", f"{ultima['nivel']:.1f} %")
    coluna_idade.metric("Idade do dado", f"{idade:.0f} s")
    if idade > LIMITE_OBSOLESCENCIA_S:
        st.warning("Dado obsoleto: o dispositivo parou de publicar?")

    st.line_chart(
        {"hora (Brasília)": [item["instante"].astimezone(BRASILIA).replace(tzinfo=None)
                             for item in historico],
         "nível (%)": [item["nivel"] for item in historico]},
        x="hora (Brasília)", y="nível (%)")
    nao_vistos = ultima["ciclo"] - historico[0]["ciclo"] + 1 - len(historico)
    st.caption(f"sessão {ultima['sessao']} · ciclo {ultima['ciclo']} · "
               f"{len(historico)} aquisições vistas · {nao_vistos} ciclos não vistos")


def main() -> None:
    st.title("Nível do tanque — LT-01")
    painel()


if __name__ == "__main__":
    main()
