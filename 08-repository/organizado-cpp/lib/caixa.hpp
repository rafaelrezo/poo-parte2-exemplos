#pragma once

#include "repositorio_pedidos.hpp"
#include <iostream>
#include <stdexcept>
#include <string>

// Cliente do contrato; não inclui repositorio_memoria.hpp.
class Caixa {
public:
    explicit Caixa(RepositorioPedidos& pedidos) : pedidos_(pedidos) {}

    int vender(const std::string& item, const std::string& setor, double valor) {
        const Pedido pedido{pedidos_.ultimo_numero() + 1, item, setor, valor};
        if (!pedidos_.adicionar(pedido)) {
            throw std::runtime_error("numero de pedido ja registrado");
        }
        std::cout << "caixa: pedido " << pedido.numero << " registrado\n";
        return pedido.numero;
    }

private:
    RepositorioPedidos& pedidos_;
};
