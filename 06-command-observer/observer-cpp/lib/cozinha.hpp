#pragma once

#include "observador.hpp"
#include <iostream>
#include <set>
#include <vector>

class Cozinha {
public:
    void assinar(Observador& observador) { observadores_.push_back(&observador); }

    void concluir(int numero) {
        if (prontos_.count(numero) > 0) {
            return;  // já estava pronto: nada mudou, nenhum evento
        }
        prontos_.insert(numero);
        std::cout << "cozinha: pedido " << numero << " pronto\n";
        for (Observador* observador : observadores_) {
            observador->receber(PedidoPronto{numero});
        }
    }

private:
    std::set<int> prontos_;                  // estado: pedidos já prontos
    std::vector<Observador*> observadores_;  // emprestados: a cozinha não os destrói
};
