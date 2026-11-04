#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

struct Aquisicao {
    std::string sessao;
    long ciclo;
    std::string timestamp;
    double nivel;
};

Aquisicao ler_aquisicao(const std::string& caminho) {
    std::ifstream arquivo(caminho);
    if (!arquivo) {
        throw std::runtime_error(caminho + " não encontrado");
    }
    const json documento = json::parse(arquivo);  // parse_error se estiver incompleto
    const json& leitura = documento.at("leituras").at(0);
    if (leitura.at("unidade").get<std::string>() != "%") {
        throw std::runtime_error("unidade diferente de %");
    }
    return Aquisicao{documento.at("sessao").get<std::string>(),
                     documento.at("ciclo").get<long>(),
                     documento.at("timestamp").get<std::string>(),
                     leitura.at("valor").get<double>()};  // type_error se não for número
}

class Consumidor {  // lembra a última aquisição para reconhecer repetição e perda
public:
    void receber(const Aquisicao& nova) {
        const bool mesma_sessao = nova.sessao == sessao_;
        if (mesma_sessao && nova.ciclo == ciclo_) {
            std::cout << "consumidor: ciclo " << nova.ciclo << " repetido, nada novo\n";
            return;
        }
        if (mesma_sessao && nova.ciclo > ciclo_ + 1) {
            std::cout << "consumidor: " << nova.ciclo - ciclo_ - 1 << " ciclo(s) não vistos\n";
        }
        sessao_ = nova.sessao;
        ciclo_ = nova.ciclo;
        std::cout << "consumidor: ciclo " << nova.ciclo << " | " << nova.timestamp
                  << " | nível " << nova.nivel << " %\n";
    }

private:
    std::string sessao_;
    long ciclo_ = 0;
};

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "uso: ./consumidor_nivel LEITURAS INTERVALO_MS\n";
        return 2;
    }
    const int leituras = std::stoi(argv[1]);
    const std::chrono::milliseconds intervalo(std::stoi(argv[2]));
    Consumidor consumidor;
    for (int i = 0; i < leituras; ++i) {
        try {
            consumidor.receber(ler_aquisicao("aquisicao.json"));
        } catch (const std::exception& erro) {  // json::exception deriva de std::exception
            std::cout << "consumidor: recusado (" << erro.what() << ")\n";
        }
        std::this_thread::sleep_for(intervalo);
    }
    return 0;
}
