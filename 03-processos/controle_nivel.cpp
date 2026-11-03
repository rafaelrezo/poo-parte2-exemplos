#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

class SensorNivel {  // abstração definida pelo controle: nível em %
public:
    virtual ~SensorNivel() = default;
    virtual double ler() = 0;
};

class SensorNivelSimulado : public SensorNivel {  // o dublê da aula 02
public:
    explicit SensorNivelSimulado(double nivel) : nivel_(nivel) {}
    double ler() override { return nivel_; }

private:
    double nivel_;
};

class SensorNivelArquivo : public SensorNivel {  // lê o que outro programa escreveu
public:
    explicit SensorNivelArquivo(std::string caminho) : caminho_(std::move(caminho)) {}

    double ler() override {
        std::ifstream arquivo(caminho_);
        if (!arquivo) {
            throw std::runtime_error(caminho_ + " não encontrado");
        }
        std::string chave_nivel;
        std::string chave_unidade;
        std::string unidade;
        double nivel = 0.0;
        arquivo >> chave_nivel >> nivel >> chave_unidade >> unidade;
        if (!arquivo || chave_nivel != "nivel" || chave_unidade != "unidade") {
            throw std::runtime_error(caminho_ + " fora do formato combinado");
        }
        if (unidade != "%") {
            throw std::runtime_error("unidade '" + unidade + "' recebida; o controle espera %");
        }
        return nivel;
    }

private:
    std::string caminho_;
};

class ControleNivel {
public:
    ControleNivel(SensorNivel& sensor, double limite) : sensor_(sensor), limite_(limite) {}

    std::string decidir() {
        if (sensor_.ler() > limite_) {
            return "alarme de nível alto";
        }
        return "normal";
    }

private:
    SensorNivel& sensor_;
    double limite_;
};

int main() {
    for (double valor : {79.0, 80.0, 81.0}) {
        SensorNivelSimulado simulado(valor);
        ControleNivel controle(simulado, 80.0);
        std::cout << "simulado " << valor << " % -> " << controle.decidir() << '\n';
    }

    SensorNivelArquivo arquivo("nivel.txt");
    ControleNivel controle(arquivo, 80.0);
    try {
        const std::string decisao = controle.decidir();
        std::cout << "nivel.txt -> " << decisao << '\n';
    } catch (const std::runtime_error& erro) {
        std::cout << "nivel.txt -> erro: " << erro.what() << '\n';
    }
    return 0;
}
