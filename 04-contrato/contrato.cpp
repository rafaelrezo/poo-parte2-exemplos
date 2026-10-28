#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

struct LeituraRecebida {
    double valor;
    std::string unidade;
};

class Nivel {
    double valor_ = 0;
public:
    void atualizar(const LeituraRecebida& leitura) {
        if (leitura.unidade != "%" || !std::isfinite(leitura.valor)
            || leitura.valor < 0 || leitura.valor > 100) {
            throw std::invalid_argument("leitura de nivel invalida");
        }
        valor_ = leitura.valor;
    }
    double valor() const { return valor_; }
};

int main() {
    Nivel nivel;
    nivel.atualizar(LeituraRecebida{48.5, "%"});
    try {
        nivel.atualizar(LeituraRecebida{0.5, "fracao"});
    } catch (const std::invalid_argument& erro) {
        std::cout << "REJEITADO: " << erro.what() << '\n';
    }
    std::cout << "ultimo valor valido: " << nivel.valor() << " %\n";
}
