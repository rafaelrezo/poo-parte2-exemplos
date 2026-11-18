#pragma once

#include "frete.hpp"

class Retirada : public Frete {
public:
    double calcular(double) const override { return 0.0; }
};

class PorPeso : public Frete {
public:
    double calcular(double peso_kg) const override { return 8.0 + 4.0 * peso_kg; }
};

class PorFaixa : public Frete {
public:
    double calcular(double peso_kg) const override {
        if (peso_kg <= 1.0) {
            return 15.0;
        }
        if (peso_kg <= 5.0) {
            return 25.0;
        }
        return 35.0;
    }
};
