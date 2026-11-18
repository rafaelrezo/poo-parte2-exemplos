#pragma once

#include <string>

class Comando {
public:
    virtual ~Comando() = default;
    virtual void executar() = 0;
    virtual std::string descrever() const = 0;
};
