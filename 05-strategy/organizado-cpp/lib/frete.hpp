#pragma once

class Frete {
public:
    virtual ~Frete() = default;
    virtual double calcular(double peso_kg) const = 0;
};
