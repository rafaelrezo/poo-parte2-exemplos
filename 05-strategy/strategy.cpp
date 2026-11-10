#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>

// Estratégia: o contrato comum a todas as modalidades de frete
class Frete {
public:
    virtual ~Frete() = default;
    virtual double calcular(double peso_kg) const = 0;
};

// Estratégias concretas: uma classe por algoritmo
class Retirada : public Frete {
public:
    double calcular(double) const override { return 0.0; }
};

class PorPeso : public Frete {
public:
    double calcular(double peso_kg) const override { return 8.0 + 4.0 * peso_kg; }
};

class PorFaixa : public Frete {
public:
    double calcular(double peso_kg) const override {
        if (peso_kg <= 1.0) {
            return 15.0;
        }
        if (peso_kg <= 5.0) {
            return 25.0;
        }
        return 35.0;
    }
};

// Contexto: cuida do pedido e delega o cálculo do frete
class Pedido {
public:
    Pedido(double produtos, double peso_kg, std::unique_ptr<Frete> frete)
        : produtos_(produtos), peso_kg_(peso_kg), frete_(std::move(frete)) {
        if (produtos_ < 0.0 || peso_kg_ <= 0.0 || !frete_) {
            throw std::invalid_argument("pedido com valor, peso ou frete inválido");
        }
    }

    double frete() const { return frete_->calcular(peso_kg_); }
    double total() const { return produtos_ + frete(); }

private:
    double produtos_;
    double peso_kg_;
    std::unique_ptr<Frete> frete_;
};

// Montagem: o único lugar que conhece as modalidades concretas
std::unique_ptr<Frete> criar_frete(const std::string& nome) {
    if (nome == "retirada") {
        return std::make_unique<Retirada>();
    }
    if (nome == "por_peso") {
        return std::make_unique<PorPeso>();
    }
    if (nome == "por_faixa") {
        return std::make_unique<PorFaixa>();
    }
    throw std::invalid_argument("modalidade de frete desconhecida: " + nome);
}

int main() {
    std::printf("peso  retirada  por_peso  por_faixa\n");
    for (double peso : {0.5, 3.0, 8.0}) {
        Pedido retirada{100.0, peso, criar_frete("retirada")};
        Pedido por_peso{100.0, peso, criar_frete("por_peso")};
        Pedido por_faixa{100.0, peso, criar_frete("por_faixa")};
        std::printf("%4.1f  %8.2f  %8.2f  %9.2f\n", peso, retirada.frete(),
                    por_peso.frete(), por_faixa.frete());
    }
    Pedido exemplo{100.0, 3.0, criar_frete("por_peso")};
    std::printf("total de um pedido de 100.00 com 3 kg, por peso: %.2f\n", exemplo.total());
}
