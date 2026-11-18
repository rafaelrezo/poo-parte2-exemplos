#include "lib/caixa.hpp"
#include "lib/relatorio.hpp"
#include "lib/repositorio_memoria.hpp"
#include <iostream>

int main() {
    // Só a montagem escolhe o armazenamento concreto.
    RepositorioMemoria pedidos;
    Caixa caixa{pedidos};
    caixa.vender("X-burguer", "cozinha", 18.0);
    caixa.vender("suco de laranja", "bar", 7.5);
    caixa.vender("misto quente", "cozinha", 12.0);

    if (const auto pedido = pedidos.buscar(2)) {
        std::cout << "pedido 2: " << pedido->item << " no " << pedido->setor << '\n';
    }
    const bool repetido = pedidos.adicionar(*pedidos.buscar(1));
    std::cout << "adicionar o pedido 1 de novo: "
              << (repetido ? "gravou" : "ignorado") << '\n';
    Relatorio{pedidos}.imprimir();
}
