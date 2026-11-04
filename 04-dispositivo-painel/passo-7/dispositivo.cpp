#include <algorithm>
#include <chrono>
#include <cmath>
#include <ctime>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>

#include <nlohmann/json.hpp>

using json = nlohmann::ordered_json;  // mantém os campos na ordem em que foram escritos
using std::chrono::system_clock;

std::string timestamp_utc(system_clock::time_point instante) {  // ISO 8601 em UTC
    const std::time_t segundos = system_clock::to_time_t(instante);
    const std::tm utc = *std::gmtime(&segundos);
    std::ostringstream saida;
    saida << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return saida.str();
}

void gravar_atomico(const std::filesystem::path& destino, const json& documento) {
    const std::filesystem::path temporario = destino.string() + ".tmp";
    {
        std::ofstream arquivo(temporario);
        arquivo << documento.dump(2) << '\n';
    }  // o temporário é fechado aqui, já completo
    std::filesystem::rename(temporario, destino);  // troca o arquivo inteiro de uma vez
}

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

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "uso: ./dispositivo CICLOS INTERVALO_MS\n";
        return 2;
    }
    const int ciclos = std::stoi(argv[1]);
    const std::chrono::milliseconds intervalo(std::stoi(argv[2]));
    const std::size_t maximo_medicoes = 60;  // a série guarda só as 60 mais recentes
    DispositivoNivel dispositivo(50.0, 7);

    json serie = {{"dispositivo", "LT-01"}, {"grandeza", "nivel"}, {"unidade", "%"},
                  {"medicoes", json::array()}};

    for (int ciclo = 1; ciclo <= ciclos; ++ciclo) {
        const json medicao = {{"ciclo", ciclo},
                              {"timestamp", timestamp_utc(system_clock::now())},
                              {"valor", dispositivo.medir()}};
        json& medicoes = serie["medicoes"];
        medicoes.push_back(medicao);
        if (medicoes.size() > maximo_medicoes) {
            medicoes.erase(medicoes.begin());  // descarta a mais antiga
        }
        gravar_atomico("serie_nivel.json", serie);  // publica a cada ciclo
        std::cout << medicao.dump() << std::endl;   // endl mostra a linha na hora
        std::this_thread::sleep_for(intervalo);
    }
    return 0;
}
