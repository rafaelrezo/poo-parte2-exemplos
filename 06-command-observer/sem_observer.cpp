#include <iostream>

class Painel {
public:
    void mostrar_pronto(int numero) { std::cout << "  painel: PRONTO " << numero << '\n'; }
};

class Aplicativo {
public:
    void avisar_cliente(int numero) {
        std::cout << "  app: pedido " << numero << " pronto, pode retirar\n";
    }
};

class Cozinha {
public:
    Cozinha(Painel& painel, Aplicativo& app) : painel_(painel), app_(app) {}

    void concluir(int numero) {
        std::cout << "cozinha: pedido " << numero << " pronto\n";
        painel_.mostrar_pronto(numero);
        app_.avisar_cliente(numero);
    }

private:
    Painel& painel_;
    Aplicativo& app_;
};

int main() {
    Painel painel;
    Aplicativo app;
    Cozinha cozinha{painel, app};
    cozinha.concluir(1);
    cozinha.concluir(2);
}
