#pragma once

#include "pedido.hpp"
#include <map>
#include <optional>
#include <string>

// Contrato conhecido pelos clientes; não escolhe onde os pedidos ficam.
class RepositorioPedidos {
public:
    virtual ~RepositorioPedidos() = default;
    virtual bool adicionar(const Pedido& pedido) = 0;
    virtual std::optional<Pedido> buscar(int numero) const = 0;
    virtual int ultimo_numero() const = 0;
    virtual std::map<std::string, double> faturamento_por_setor() const = 0;
};
