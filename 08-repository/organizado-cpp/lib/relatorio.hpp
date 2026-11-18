#pragma once

#include "repositorio_pedidos.hpp"
#include <iomanip>
#include <iostream>

// Outro cliente do mesmo contrato; não conhece o armazenamento.
class Relatorio {
public:
    explicit Relatorio(const RepositorioPedidos& pedidos) : pedidos_(pedidos) {}

    void imprimir() const {
        std::cout << std::fixed << std::setprecision(2) << "faturamento por setor:\n";
        for (const auto& [setor, total] : pedidos_.faturamento_por_setor()) {
            std::cout << "  " << setor << ": R$ " << total << '\n';
        }
    }

private:
    const RepositorioPedidos& pedidos_;
};
