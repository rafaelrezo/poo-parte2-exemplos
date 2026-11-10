#include <cstdio>
#include <stdexcept>

enum class TipoFrete { Retirada, PorPeso, PorFaixa };

class Pedido {
public:
    Pedido(double produtos, double peso_kg, TipoFrete tipo)
        : produtos_(produtos), peso_kg_(peso_kg), tipo_(tipo) {
        if (produtos_ < 0.0 || peso_kg_ <= 0.0) {
            throw std::invalid_argument("pedido com valor ou peso inválido");
        }
    }

    double frete() const {
        if (tipo_ == TipoFrete::Retirada) {
            return 0.0;
        }
        if (tipo_ == TipoFrete::PorPeso) {
            return 8.0 + 4.0 * peso_kg_;
        }
        // TipoFrete::PorFaixa
        if (peso_kg_ <= 1.0) {
            return 15.0;
        }
        if (peso_kg_ <= 5.0) {
            return 25.0;
        }
        return 35.0;
    }

    double total() const { return produtos_ + frete(); }

private:
    double produtos_;
    double peso_kg_;
    TipoFrete tipo_;
};

int main() {
    std::printf("peso  retirada  por_peso  por_faixa\n");
    for (double peso : {0.5, 3.0, 8.0}) {
        Pedido retirada{100.0, peso, TipoFrete::Retirada};
        Pedido por_peso{100.0, peso, TipoFrete::PorPeso};
        Pedido por_faixa{100.0, peso, TipoFrete::PorFaixa};
        std::printf("%4.1f  %8.2f  %8.2f  %9.2f\n", peso, retirada.frete(),
                    por_peso.frete(), por_faixa.frete());
    }
    Pedido exemplo{100.0, 3.0, TipoFrete::PorPeso};
    std::printf("total de um pedido de 100.00 com 3 kg, por peso: %.2f\n", exemplo.total());
}
