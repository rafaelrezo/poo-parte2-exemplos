#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>

class DispositivoNivel {  // simula o transmissor de nível LT-01
public:
    DispositivoNivel(double nivel_inicial, unsigned semente)
        : nivel_(nivel_inicial), gerador_(semente), variacao_(-2.0, 2.0) {}

    double medir() {  // o novo nível é o anterior mais uma pequena variação
        nivel_ = std::clamp(nivel_ + variacao_(gerador_), 0.0, 100.0);
        return std::round(nivel_ * 100.0) / 100.0;  // duas casas decimais
    }

private:
    double nivel_;
    std::mt19937 gerador_;
    std::uniform_real_distribution<double> variacao_;
};

int main() {
    DispositivoNivel dispositivo(50.0, 7);
    for (int ciclo = 1; ciclo <= 10; ++ciclo) {
        std::cout << "ciclo " << ciclo << ": nível " << dispositivo.medir() << " %\n";
    }
    return 0;
}
