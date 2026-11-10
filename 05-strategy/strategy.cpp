#include <algorithm>
#include <cstdio>
#include <deque>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Estratégia: o contrato comum a todos os filtros
class FiltroSinal {
public:
    virtual ~FiltroSinal() = default;
    virtual double filtrar(double bruto) = 0;
};

// Estratégias concretas: cada uma guarda só o que o seu algoritmo usa
class UltimoValor : public FiltroSinal {
public:
    double filtrar(double bruto) override { return bruto; }
};

class MediaMovel : public FiltroSinal {
public:
    explicit MediaMovel(std::size_t janela) : janela_(janela) {
        if (janela_ == 0) {
            throw std::invalid_argument("a janela precisa ter ao menos uma leitura");
        }
    }

    double filtrar(double bruto) override {
        recentes_.push_back(bruto);
        if (recentes_.size() > janela_) {
            recentes_.pop_front();
        }
        double soma = 0.0;
        for (double valor : recentes_) {
            soma += valor;
        }
        return soma / recentes_.size();
    }

private:
    std::size_t janela_;
    std::deque<double> recentes_;
};

class Mediana : public FiltroSinal {
public:
    explicit Mediana(std::size_t janela) : janela_(janela) {
        if (janela_ == 0) {
            throw std::invalid_argument("a janela precisa ter ao menos uma leitura");
        }
    }

    double filtrar(double bruto) override {
        recentes_.push_back(bruto);
        if (recentes_.size() > janela_) {
            recentes_.pop_front();
        }
        std::vector<double> ordenados(recentes_.begin(), recentes_.end());
        std::sort(ordenados.begin(), ordenados.end());
        const std::size_t meio = ordenados.size() / 2;
        if (ordenados.size() % 2 == 0) {
            return (ordenados[meio - 1] + ordenados[meio]) / 2.0;
        }
        return ordenados[meio];
    }

private:
    std::size_t janela_;
    std::deque<double> recentes_;
};

// Contexto: valida a leitura e delega o tratamento do sinal
class CanalNivel {
public:
    explicit CanalNivel(std::unique_ptr<FiltroSinal> filtro) : filtro_(std::move(filtro)) {
        if (!filtro_) {
            throw std::invalid_argument("o canal precisa de um filtro");
        }
    }

    double receber(double bruto) {
        if (bruto < 0.0 || bruto > 100.0) {
            throw std::out_of_range("nível fora de 0 a 100 %");
        }
        return filtro_->filtrar(bruto);
    }

private:
    std::unique_ptr<FiltroSinal> filtro_;
};

// Montagem: o único lugar que conhece os filtros concretos
std::unique_ptr<FiltroSinal> criar_filtro(const std::string& nome) {
    if (nome == "ultimo") {
        return std::make_unique<UltimoValor>();
    }
    if (nome == "media3") {
        return std::make_unique<MediaMovel>(3);
    }
    if (nome == "mediana3") {
        return std::make_unique<Mediana>(3);
    }
    throw std::invalid_argument("filtro desconhecido: " + nome);
}

int main() {
    const std::vector<double> leituras{48.0, 48.6, 47.8, 48.4, 93.0, 48.2, 47.6, 48.0};

    CanalNivel ultimo{criar_filtro("ultimo")};
    CanalNivel media{criar_filtro("media3")};
    CanalNivel mediana{criar_filtro("mediana3")};

    std::printf("bruto  ultimo  media3  mediana3\n");
    for (double bruto : leituras) {
        std::printf("%5.1f  %6.1f  %6.1f  %8.1f\n", bruto, ultimo.receber(bruto),
                    media.receber(bruto), mediana.receber(bruto));
    }
}
