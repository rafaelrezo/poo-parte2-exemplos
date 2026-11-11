import sqlite3
from contextlib import closing
from dataclasses import asdict
from pathlib import Path

import streamlit as st

from repository import HistoricoSQLite, exportar_csv


def main():
    st.title("Histórico de nível — consulta")
    caminho = Path(st.text_input("Banco SQLite", "historico.db"))
    if not caminho.is_file():
        st.info("Banco ausente. A tela não cria aquisições.")
        return
    try:
        with closing(sqlite3.connect(caminho)) as conexao:
            itens = HistoricoSQLite(conexao).listar()
    except (sqlite3.Error, ValueError) as erro:
        st.error(f"Histórico indisponível: {erro}")
        return
    if not itens:
        st.info("Nenhuma aquisição registrada.")
        return
    st.dataframe([asdict(item) for item in itens])
    sessoes = sorted({item.sessao for item in itens})
    sessao = st.selectbox("Sessão para o gráfico", sessoes)
    selecionados = [item for item in itens if item.sessao == sessao]
    st.line_chart({"ciclo": [item.ciclo for item in selecionados],
                   "nivel": [item.nivel for item in selecionados]}, x="ciclo", y="nivel")
    st.download_button("Baixar CSV da sessão", exportar_csv(selecionados),
                       "historico.csv", "text/csv")


if __name__ == "__main__":
    main()
