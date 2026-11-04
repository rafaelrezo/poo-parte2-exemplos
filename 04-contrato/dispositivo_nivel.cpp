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

using json = nlohmann::json;
using std::chrono::system_clock;

std::string para_texto(system_clock::time_point instante) {  // ISO 8601 em UTC (§4)
    const std::time_t segundos = system_clock::to_time_t(instante);
    const std::tm utc = *std::gmtime(&segundos);
    std::ostringstream saida;
    saida << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return saida.str();
}

void publicar_atomico(const std::filesystem::path& destino, const json& documento) {  // §8
    const std::filesystem::path temporario = destino.string() + ".tmp";
    {
        std::ofstream arquivo(temporario);
        arquivo << documento.dump() << '\n';
    }  // o arquivo é fechado aqui, antes da troca
    std::filesystem::rename(temporario, destino);  // troca o arquivo inteiro de uma vez
}

class DispositivoNivel {  // simula o transmissor LT-01
public:
    DispositivoNivel(double nivel_inicial, unsigned semente)
        : nivel_(nivel_inicial), gerador_(semente), variacao_(-2.0, 2.0) {}

    double medir() {  // a cada ciclo, o nível varia ao acaso até 2 pontos
        nivel_ = std::clamp(nivel_ + variacao_(gerador_), 0.0, 100.0);
        return std::round(nivel_ * 100.0) / 100.0;
    }

private:
    double nivel_;
    std::mt19937 gerador_;  // mesma semente, mesma sequência
    std::uniform_real_distribution<double> variacao_;
};

int main(int argc, char* argv[]) {
    if (argc < 3 || argc > 4) {
        std::cout << "uso: ./dispositivo_nivel CICLOS INTERVALO_MS [SEMENTE]\n";
        return 2;
    }
    const int ciclos = std::stoi(argv[1]);
    const std::chrono::milliseconds intervalo(std::stoi(argv[2]));
    const unsigned semente = argc == 4 ? static_cast<unsigned>(std::stoul(argv[3])) : 7U;

    const std::string sessao = "lt01-" + std::to_string(std::time(nullptr));  // nova a cada execução
    DispositivoNivel dispositivo(50.0, semente);

    for (int ciclo = 1; ciclo <= ciclos; ++ciclo) {
        const double nivel = dispositivo.medir();
        const std::string instante = para_texto(system_clock::now());
        const json leitura = {{"tag", "LT-01"}, {"tipo", "nivel"}, {"valor", nivel},
                              {"unidade", "%"}, {"status", "operando"}};
        const json aquisicao = {{"versao", 1}, {"sessao", sessao}, {"ciclo", ciclo},
                                {"timestamp", instante}, {"leituras", json::array({leitura})}};
        publicar_atomico("aquisicao.json", aquisicao);
        std::cout << "dispositivo: ciclo " << std::setw(3) << ciclo << ' ' << instante
                  << " nível " << nivel << " %" << std::endl;
        std::this_thread::sleep_for(intervalo);
    }
    return 0;
}
