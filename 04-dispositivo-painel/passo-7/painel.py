from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

from serie import carregar_serie

BRASILIA = timezone(timedelta(hours=-3))  # só para exibir; o arquivo fica em UTC
LIMITE_OBSOLESCENCIA_S = 5  # sem medição nova há mais de 5 s: dado antigo


@st.fragment(run_every=1.0)  # reexecuta esta função a cada segundo
def grafico() -> None:
    try:
        serie = carregar_serie(Path("serie_nivel.json"))
    except FileNotFoundError:
        st.info("serie_nivel.json não encontrado: execute o dispositivo primeiro.")
        return
    except ValueError as erro:
        st.error(f"Série recusada: {erro}")
        return
    if not serie:
        st.info("A série ainda não tem medições.")
        return

    ultima = serie[-1]
    idade = (datetime.now(timezone.utc) - ultima.instante).total_seconds()
    coluna_valor, coluna_idade = st.columns(2)
    coluna_valor.metric("Última medição", f"{ultima.valor:.2f} %")
    coluna_idade.metric("Idade da medição", f"{idade:.0f} s")
    if idade > LIMITE_OBSOLESCENCIA_S:
        st.warning("Dado antigo: o dispositivo parou de publicar?")

    horarios = [m.instante.astimezone(BRASILIA).replace(tzinfo=None) for m in serie]
    st.line_chart({"hora (Brasília)": horarios, "nível (%)": [m.valor for m in serie]},
                  x="hora (Brasília)", y="nível (%)")
    st.caption(f"{len(serie)} medições · ciclo {ultima.ciclo}")


def main() -> None:
    st.title("Nível do tanque — LT-01")
    grafico()


if __name__ == "__main__":
    main()
