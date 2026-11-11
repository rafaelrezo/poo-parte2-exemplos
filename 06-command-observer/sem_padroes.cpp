#include <iostream>
#include <string>

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

    void preparar(int numero, const std::string& item) {
        std::cout << "  cozinha: preparou " << item << '\n';
        painel_.mostrar_pronto(numero);
        app_.avisar_cliente(numero);
    }

private:
    Painel& painel_;
    Aplicativo& app_;
};

class Caixa {
public:
    explicit Caixa(Cozinha& cozinha) : cozinha_(cozinha) {}

    void vender(const std::string& item) {
        ++numero_;
        std::cout << "caixa: pedido " << numero_ << ", " << item << '\n';
        cozinha_.preparar(numero_, item);
        std::cout << "caixa: pronto para o proximo cliente\n";
    }

private:
    Cozinha& cozinha_;
    int numero_ = 0;
};

int main() {
    Painel painel;
    Aplicativo app;
    Cozinha cozinha{painel, app};
    Caixa caixa{cozinha};
    caixa.vender("X-burguer");
    caixa.vender("misto quente");
}
