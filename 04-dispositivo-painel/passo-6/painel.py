from datetime import timedelta, timezone
from pathlib import Path

import streamlit as st

from serie import carregar_serie

BRASILIA = timezone(timedelta(hours=-3))  # só para exibir; o arquivo fica em UTC


def main() -> None:
    st.title("Nível do tanque — LT-01")
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
    st.metric("Última medição", f"{ultima.valor:.2f} %")

    horarios = [m.instante.astimezone(BRASILIA).replace(tzinfo=None) for m in serie]
    st.line_chart({"hora (Brasília)": horarios, "nível (%)": [m.valor for m in serie]},
                  x="hora (Brasília)", y="nível (%)")

    st.dataframe([{"ciclo": m.ciclo, "hora (Brasília)": h, "nível (%)": m.valor}
                  for m, h in zip(serie, horarios)])


if __name__ == "__main__":
    main()
