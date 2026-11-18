#include "lib/comandos.hpp"
#include "lib/fila.hpp"
#include "lib/receptores.hpp"
#include <iostream>
#include <memory>

int main() {
    Cozinha cozinha;
    Bar bar;
    Fila fila;

    // Cliente: o caixa cria cada comanda, ligada ao seu receptor, e a entrega à fila
    fila.receber(std::make_unique<PrepararLanche>(cozinha, 1, "X-burguer"));
    fila.receber(std::make_unique<PrepararBebida>(bar, 2, "suco de laranja"));
    fila.receber(std::make_unique<PrepararLanche>(cozinha, 3, "misto quente"));
    std::cout << "caixa: " << fila.pendentes() << " pedidos registrados, nenhum preparado ainda\n";

    // Mais tarde, quando há quem prepare, a fila executa as comandas na ordem
    fila.atender_todos();

    std::cout << "historico da fila:\n";
    for (const auto& linha : fila.historico()) {
        std::cout << "  " << linha << '\n';
    }
}
