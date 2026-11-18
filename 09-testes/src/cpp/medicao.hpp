#pragma once

#include <cmath>
#include <stdexcept>

class Medicao {
    double valor_;

public:
    explicit Medicao(double valor) : valor_(0) {
        if (!atualizar(valor)) {
            throw std::invalid_argument("medicao inicial invalida");
        }
    }

    bool atualizar(double valor) {
        if (!std::isfinite(valor) || valor < 0 || valor > 100) {
            return false;
        }
        valor_ = valor;
        return true;
    }

    double valor() const { return valor_; }
};
