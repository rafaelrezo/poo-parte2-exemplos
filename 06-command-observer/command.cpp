#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

// Receptores: sabem fazer o trabalho; não sabem que existe uma fila
class Cozinha {
public:
    void preparar_lanche(int numero, const std::string& lanche) {
        std::cout << "  cozinha: " << lanche << " (pedido " << numero << ")\n";
    }
};

class Bar {
public:
    void preparar_bebida(int numero, const std::string& bebida) {
        std::cout << "  bar: " << bebida << " (pedido " << numero << ")\n";
    }
};

// Comando: o contrato comum de toda solicitação
class Comando {
public:
    virtual ~Comando() = default;
    virtual void executar() = 0;
    virtual std::string descrever() const = 0;
};

// Comandos concretos: guardam o receptor e os dados da solicitação
class PrepararLanche : public Comando {
public:
    PrepararLanche(Cozinha& cozinha, int numero, std::string lanche)
        : cozinha_(cozinha), numero_(numero), lanche_(std::move(lanche)) {}

    void executar() override { cozinha_.preparar_lanche(numero_, lanche_); }
    std::string descrever() const override {
        return "pedido " + std::to_string(numero_) + ": " + lanche_ + " na cozinha";
    }

private:
    Cozinha& cozinha_;
    int numero_;
    std::string lanche_;
};

class PrepararBebida : public Comando {
public:
    PrepararBebida(Bar& bar, int numero, std::string bebida)
        : bar_(bar), numero_(numero), bebida_(std::move(bebida)) {}

    void executar() override { bar_.preparar_bebida(numero_, bebida_); }
    std::string descrever() const override {
        return "pedido " + std::to_string(numero_) + ": " + bebida_ + " no bar";
    }

private:
    Bar& bar_;
    int numero_;
    std::string bebida_;
};

// Invocador: guarda as comandas e decide quando executá-las; só conhece Comando
class Fila {
public:
    void receber(std::unique_ptr<Comando> comando) { pendentes_.push_back(std::move(comando)); }

    std::size_t pendentes() const { return pendentes_.size(); }

    void atender_todos() {
        for (const auto& comando : pendentes_) {
            comando->executar();
            historico_.push_back(comando->descrever());
        }
        pendentes_.clear();
    }

    const std::vector<std::string>& historico() const { return historico_; }

private:
    std::vector<std::unique_ptr<Comando>> pendentes_;
    std::vector<std::string> historico_;
};

int main() {
    Cozinha cozinha;
    Bar bar;
    Fila fila;

    // Cliente: o caixa cria cada comanda, ligada ao seu receptor, e a entrega à fila
    fila.receber(std::make_unique<PrepararLanche>(cozinha, 1, "X-burguer"));
    fila.receber(std::make_unique<PrepararBebida>(bar, 2, "suco de laranja"));
    fila.receber(std::make_unique<PrepararLanche>(cozinha, 3, "misto quente"));
    std::cout << "caixa: " << fila.pendentes() << " pedidos registrados, nenhum preparado ainda\n";

    // Mais tarde, quando há quem prepare, a fila executa as comandas na ordem
    fila.atender_todos();

    std::cout << "historico da fila:\n";
    for (const auto& linha : fila.historico()) {
        std::cout << "  " << linha << '\n';
    }
}
