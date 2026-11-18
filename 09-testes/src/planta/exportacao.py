import csv
import io


def exportar_csv(aquisicoes):
    saida = io.StringIO(newline="")
    escritor = csv.writer(saida, lineterminator="\n")
    escritor.writerow(["sessao", "ciclo", "nivel"])
    for aquisicao in aquisicoes:
        escritor.writerow([aquisicao.sessao, aquisicao.ciclo, aquisicao.nivel])
    return saida.getvalue()
