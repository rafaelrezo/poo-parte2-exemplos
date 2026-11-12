#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <string>

// Entidade: o objeto do domínio que o repositório guarda
struct Pedido {
    int numero;
    std::string item;
    std::string setor;
    double valor;
};

// Repositório: o contrato que o domínio conhece, escrito na linguagem do domínio
class RepositorioPedidos {
public:
    virtual ~RepositorioPedidos() = default;
    virtual bool adicionar(const Pedido& pedido) = 0;  // false se o número já existia
    virtual std::optional<Pedido> buscar(int numero) const = 0;
    virtual int ultimo_numero() const = 0;
    virtual std::map<std::string, double> faturamento_por_setor() const = 0;
};

// Implementação em memória; uma versão com SQLite implementaria o mesmo contrato
class RepositorioMemoria : public RepositorioPedidos {
public:
    bool adicionar(const Pedido& pedido) override {
        return pedidos_.emplace(pedido.numero, pedido).second;
    }

    std::optional<Pedido> buscar(int numero) const override {
        const auto encontrado = pedidos_.find(numero);
        if (encontrado == pedidos_.end()) {
            return std::nullopt;
        }
        return encontrado->second;
    }

    int ultimo_numero() const override {
        return pedidos_.empty() ? 0 : pedidos_.rbegin()->first;
    }

    std::map<std::string, double> faturamento_por_setor() const override {
        std::map<std::string, double> totais;
        for (const auto& [numero, pedido] : pedidos_) {
            totais[pedido.setor] += pedido.valor;
        }
        return totais;
    }

private:
    std::map<int, Pedido> pedidos_;  // chave: o número do pedido
};

// Cliente: registra vendas; conhece só o contrato
class Caixa {
public:
    explicit Caixa(RepositorioPedidos& pedidos) : pedidos_(pedidos) {}

    int vender(const std::string& item, const std::string& setor, double valor) {
        const Pedido pedido{pedidos_.ultimo_numero() + 1, item, setor, valor};
        pedidos_.adicionar(pedido);
        std::cout << "caixa: pedido " << pedido.numero << " registrado\n";
        return pedido.numero;
    }

private:
    RepositorioPedidos& pedidos_;
};

int main() {
    RepositorioMemoria pedidos;
    Caixa caixa{pedidos};
    caixa.vender("X-burguer", "cozinha", 18.0);
    caixa.vender("suco de laranja", "bar", 7.5);
    caixa.vender("misto quente", "cozinha", 12.0);

    if (const auto pedido = pedidos.buscar(2)) {
        std::cout << "pedido 2: " << pedido->item << " no " << pedido->setor << '\n';
    }
    const bool repetido = pedidos.adicionar(*pedidos.buscar(1));
    std::cout << "adicionar o pedido 1 de novo: " << (repetido ? "gravou" : "ignorado") << '\n';

    std::cout << std::fixed << std::setprecision(2) << "faturamento por setor:\n";
    for (const auto& [setor, total] : pedidos.faturamento_por_setor()) {
        std::cout << "  " << setor << ": R$ " << total << '\n';
    }
}
