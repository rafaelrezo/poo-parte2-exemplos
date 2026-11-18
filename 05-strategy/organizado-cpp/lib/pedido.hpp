#pragma once

#include "frete.hpp"
#include <memory>
#include <stdexcept>
#include <utility>

class Pedido {
public:
    Pedido(double produtos, double peso_kg, std::unique_ptr<Frete> frete)
        : produtos_(produtos), peso_kg_(peso_kg), frete_(std::move(frete)) {
        if (produtos_ < 0.0 || peso_kg_ <= 0.0 || !frete_) {
            throw std::invalid_argument("pedido com valor, peso ou frete inválido");
        }
    }

    double frete() const { return frete_->calcular(peso_kg_); }
    double total() const { return produtos_ + frete(); }

private:
    double produtos_;
    double peso_kg_;
    std::unique_ptr<Frete> frete_;
};
