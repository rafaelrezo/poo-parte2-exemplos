#pragma once

#include "evento.hpp"

class Observador {
public:
    virtual ~Observador() = default;
    virtual void receber(const PedidoPronto& evento) = 0;
};
