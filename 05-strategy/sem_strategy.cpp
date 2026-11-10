#include <algorithm>
#include <cstdio>
#include <deque>
#include <stdexcept>
#include <vector>

enum class ModoFiltro { UltimoValor, MediaMovel, Mediana };

class CanalNivel {
public:
    CanalNivel(ModoFiltro modo, std::size_t janela) : modo_(modo), janela_(janela) {
        if (janela_ == 0) {
            throw std::invalid_argument("a janela precisa ter ao menos uma leitura");
        }
    }

    double receber(double bruto) {
        if (bruto < 0.0 || bruto > 100.0) {
            throw std::out_of_range("nível fora de 0 a 100 %");
        }
        if (modo_ == ModoFiltro::UltimoValor) {
            return bruto;
        }
        recentes_.push_back(bruto);
        if (recentes_.size() > janela_) {
            recentes_.pop_front();
        }
        if (modo_ == ModoFiltro::MediaMovel) {
            double soma = 0.0;
            for (double valor : recentes_) {
                soma += valor;
            }
            return soma / recentes_.size();
        }
        // ModoFiltro::Mediana: acrescentado depois, dentro do mesmo método
        std::vector<double> ordenados(recentes_.begin(), recentes_.end());
        std::sort(ordenados.begin(), ordenados.end());
        const std::size_t meio = ordenados.size() / 2;
        if (ordenados.size() % 2 == 0) {
            return (ordenados[meio - 1] + ordenados[meio]) / 2.0;
        }
        return ordenados[meio];
    }

private:
    ModoFiltro modo_;
    std::size_t janela_;            // ignorada no modo UltimoValor
    std::deque<double> recentes_;   // vazia no modo UltimoValor
};

int main() {
    const std::vector<double> leituras{48.0, 48.6, 47.8, 48.4, 93.0, 48.2, 47.6, 48.0};

    CanalNivel ultimo{ModoFiltro::UltimoValor, 1};
    CanalNivel media{ModoFiltro::MediaMovel, 3};
    CanalNivel mediana{ModoFiltro::Mediana, 3};

    std::printf("bruto  ultimo  media3  mediana3\n");
    for (double bruto : leituras) {
        std::printf("%5.1f  %6.1f  %6.1f  %8.1f\n", bruto, ultimo.receber(bruto),
                    media.receber(bruto), mediana.receber(bruto));
    }
}
