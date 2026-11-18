#pragma once

#include "repositorio_pedidos.hpp"
#include <map>
#include <optional>
#include <string>

// Implementação concreta: substituível sem editar Caixa ou Relatorio.
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
        for (const auto& par : pedidos_) {
            const Pedido& pedido = par.second;
            totais[pedido.setor] += pedido.valor;
        }
        return totais;
    }

private:
    std::map<int, Pedido> pedidos_;
};
