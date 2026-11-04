#include <cmath>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

struct LeituraRecebida {  // campos já extraídos do JSON pela biblioteca
    double valor;
    std::string unidade;
};

class Nivel {  // objeto do domínio: só guarda nível válido em %
public:
    void atualizar(const LeituraRecebida& leitura) {
        if (leitura.unidade != "%") {
            throw std::invalid_argument("unidade '" + leitura.unidade + "'; esperado %");
        }
        if (!std::isfinite(leitura.valor) || leitura.valor < 0 || leitura.valor > 100) {
            throw std::invalid_argument("valor fora da faixa 0 a 100");
        }
        valor_ = leitura.valor;
    }

    double valor() const { return valor_; }

private:
    double valor_ = 0.0;
};

int main() {
    const LeituraRecebida recebidas[] = {
        {48.5, "%"},
        {0.485, "fracao"},
        {185.0, "%"},
        {std::numeric_limits<double>::quiet_NaN(), "%"},
    };
    Nivel nivel;
    for (const LeituraRecebida& leitura : recebidas) {
        try {
            nivel.atualizar(leitura);
            std::cout << "ACEITO: " << leitura.valor << ' ' << leitura.unidade << '\n';
        } catch (const std::invalid_argument& erro) {
            std::cout << "RECUSADO: " << erro.what() << '\n';
        }
    }
    std::cout << "último valor válido: " << nivel.valor() << " %\n";
    return 0;
}
