#include <iostream>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

// Receptor: sabe preparar e decide se aceita cada pedido
class Cozinha {
public:
    explicit Cozinha(int paes) : paes_(paes) {}

    std::string preparar(int numero, const std::string& item) {
        if (preparados_.count(numero) > 0) {
            return "repetido, ignorado";
        }
        if (paes_ == 0) {
            return "recusado, acabou o pao";
        }
        --paes_;
        preparados_.insert(numero);
        return "pronto (" + item + ")";
    }

    std::string repor_paes(int quantidade) {
        paes_ += quantidade;
        return "estoque com " + std::to_string(paes_) + " paes";
    }

private:
    int paes_;
    std::set<int> preparados_;
};

// Comando: a solicitação como objeto, com uma única operação para executá-la
class Comando {
public:
    virtual ~Comando() = default;
    virtual std::string descrever() const = 0;
    virtual std::string executar() const = 0;
};

// Comandos concretos: guardam o receptor e os dados da solicitação
class PrepararPedido : public Comando {
public:
    PrepararPedido(Cozinha& cozinha, int numero, std::string item)
        : cozinha_(cozinha), numero_(numero), item_(std::move(item)) {}

    std::string descrever() const override { return "pedido " + std::to_string(numero_); }
    std::string executar() const override { return cozinha_.preparar(numero_, item_); }

private:
    Cozinha& cozinha_;
    int numero_;
    std::string item_;
};

class ReporPaes : public Comando {
public:
    ReporPaes(Cozinha& cozinha, int quantidade) : cozinha_(cozinha), quantidade_(quantidade) {}

    std::string descrever() const override {
        return "repor " + std::to_string(quantidade_) + " paes";
    }
    std::string executar() const override { return cozinha_.repor_paes(quantidade_); }

private:
    Cozinha& cozinha_;
    int quantidade_;
};

// Invocador: guarda as comandas e as executa na ordem, sem conhecer a cozinha
class Fila {
public:
    void receber(std::unique_ptr<Comando> comando) { pendentes_.push_back(std::move(comando)); }

    std::size_t pendentes() const { return pendentes_.size(); }

    void atender_todos() {
        for (const auto& comando : pendentes_) {
            historico_.push_back(comando->descrever() + ": " + comando->executar());
        }
        pendentes_.clear();
    }

    const std::vector<std::string>& historico() const { return historico_; }

private:
    std::vector<std::unique_ptr<Comando>> pendentes_;
    std::vector<std::string> historico_;
};

int main() {
    Cozinha cozinha{2};
    Fila fila;

    // Clientes: caixa e aplicativo criam comandas e voltam a atender
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 1, "X-burguer"));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 2, "misto quente"));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 2, "misto quente"));  // reenvio
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 3, "X-salada"));
    fila.receber(std::make_unique<ReporPaes>(cozinha, 10));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 4, "X-burguer"));
    std::cout << "na fila: " << fila.pendentes() << " comandas, nenhuma executada\n";

    fila.atender_todos();
    for (const auto& linha : fila.historico()) {
        std::cout << linha << '\n';
    }
}
