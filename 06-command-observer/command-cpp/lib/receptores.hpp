#pragma once

#include <iostream>
#include <string>

class Cozinha {
public:
    void preparar_lanche(int numero, const std::string& lanche) {
        std::cout << "  cozinha: " << lanche << " (pedido " << numero << ")\n";
    }
};

class Bar {
public:
    void preparar_bebida(int numero, const std::string& bebida) {
        std::cout << "  bar: " << bebida << " (pedido " << numero << ")\n";
    }
};
