#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>

#include <nlohmann/json.hpp>

using json = nlohmann::ordered_json;  // mantém os campos na ordem em que foram escritos

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

    json serie = {{"dispositivo", "LT-01"}, {"grandeza", "nivel"}, {"unidade", "%"},
                  {"medicoes", json::array()}};  // lista vazia, preenchida no laço

    for (int ciclo = 1; ciclo <= 10; ++ciclo) {
        const json medicao = {{"ciclo", ciclo}, {"valor", dispositivo.medir()}};
        serie["medicoes"].push_back(medicao);
    }

    std::ofstream arquivo("serie_nivel.json");
    arquivo << serie.dump(2) << '\n';  // serializa com recuo de 2 espaços
    std::cout << "serie_nivel.json gravado com " << serie["medicoes"].size() << " medições\n";
    return 0;
}
