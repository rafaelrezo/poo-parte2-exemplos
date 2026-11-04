#include <iostream>
#include <random>

int main() {
    std::mt19937 gerador(7);                                   // gerador com semente 7
    std::uniform_real_distribution<double> sorteio(0.0, 100.0);  // reais entre 0 e 100

    for (int i = 1; i <= 5; ++i) {
        std::cout << "sorteio " << i << ": " << sorteio(gerador) << '\n';
    }
    return 0;
}
