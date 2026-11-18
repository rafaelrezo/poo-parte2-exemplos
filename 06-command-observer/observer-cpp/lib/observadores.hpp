#pragma once

#include "observador.hpp"
#include <iostream>

class Painel : public Observador {
public:
    void receber(const PedidoPronto& evento) override {
        std::cout << "  painel: PRONTO " << evento.numero << '\n';
    }
};

class Aplicativo : public Observador {
public:
    void receber(const PedidoPronto& evento) override {
        std::cout << "  app: pedido " << evento.numero << " pronto, pode retirar\n";
    }
};
