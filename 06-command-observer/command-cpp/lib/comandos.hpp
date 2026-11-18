#pragma once

#include "comando.hpp"
#include "receptores.hpp"
#include <string>
#include <utility>

class PrepararLanche : public Comando {
public:
    PrepararLanche(Cozinha& cozinha, int numero, std::string lanche)
        : cozinha_(cozinha), numero_(numero), lanche_(std::move(lanche)) {}

    void executar() override { cozinha_.preparar_lanche(numero_, lanche_); }
    std::string descrever() const override {
        return "pedido " + std::to_string(numero_) + ": " + lanche_ + " na cozinha";
    }

private:
    Cozinha& cozinha_;
    int numero_;
    std::string lanche_;
};

class PrepararBebida : public Comando {
public:
    PrepararBebida(Bar& bar, int numero, std::string bebida)
        : bar_(bar), numero_(numero), bebida_(std::move(bebida)) {}

    void executar() override { bar_.preparar_bebida(numero_, bebida_); }
    std::string descrever() const override {
        return "pedido " + std::to_string(numero_) + ": " + bebida_ + " no bar";
    }

private:
    Bar& bar_;
    int numero_;
    std::string bebida_;
};
