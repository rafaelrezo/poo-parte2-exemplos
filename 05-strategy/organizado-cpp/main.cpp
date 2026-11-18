#include "lib/modalidades.hpp"
#include "lib/pedido.hpp"
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>

std::unique_ptr<Frete> criar_frete(const std::string& nome) {
    if (nome == "retirada") {
        return std::make_unique<Retirada>();
    }
    if (nome == "por_peso") {
        return std::make_unique<PorPeso>();
    }
    if (nome == "por_faixa") {
        return std::make_unique<PorFaixa>();
    }
    throw std::invalid_argument("modalidade de frete desconhecida: " + nome);
}

int main() {
    std::printf("peso  retirada  por_peso  por_faixa\n");
    for (double peso : {0.5, 3.0, 8.0}) {
        Pedido retirada{100.0, peso, criar_frete("retirada")};
        Pedido por_peso{100.0, peso, criar_frete("por_peso")};
        Pedido por_faixa{100.0, peso, criar_frete("por_faixa")};
        std::printf("%4.1f  %8.2f  %8.2f  %9.2f\n", peso, retirada.frete(),
                    por_peso.frete(), por_faixa.frete());
    }
    Pedido exemplo{100.0, 3.0, criar_frete("por_peso")};
    std::printf("total de um pedido de 100.00 com 3 kg, por peso: %.2f\n", exemplo.total());
}
