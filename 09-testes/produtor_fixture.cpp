#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <locale>
#include <stdexcept>
#include <string>

int main(int argc, char* argv[]) {
    try {
        if (argc != 2) {
            throw std::invalid_argument("informe um nivel");
        }
        std::size_t usados = 0;
        const std::string texto{argv[1]};
        const double nivel = std::stod(texto, &usados);
        if (usados != texto.size() || !std::isfinite(nivel) || nivel < 0 || nivel > 100) {
            throw std::invalid_argument("nivel invalido");
        }
        std::cout.imbue(std::locale::classic());
        std::cout << std::setprecision(std::numeric_limits<double>::max_digits10);
        std::cout << R"({"versao":1,"sessao":"ensaio","ciclo":12,)"
                  << R"("timestamp":"2026-10-21T18:00:00Z","leituras":[{)"
                  << R"("tag":"LT-01","tipo":"nivel","valor":)" << nivel
                  << R"(,"unidade":"%","status":"operando"}]})" << '\n';
        return 0;
    } catch (const std::exception& erro) {
        std::cerr << erro.what() << '\n';
        return 1;
    }
}
