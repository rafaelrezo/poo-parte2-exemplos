#include "lib/cozinha.hpp"
#include "lib/observadores.hpp"
#include <iostream>

int main() {
    Painel painel;  // criados antes da cozinha: vivem mais que ela
    Aplicativo app;
    Cozinha cozinha;
    cozinha.assinar(painel);
    cozinha.assinar(app);

    cozinha.concluir(1);
    cozinha.concluir(2);
    std::cout << "(o cozinheiro aperta de novo o botao do pedido 2)\n";
    cozinha.concluir(2);
}
