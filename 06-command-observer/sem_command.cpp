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

class Caixa {
public:
    Caixa(Cozinha& cozinha, Bar& bar) : cozinha_(cozinha), bar_(bar) {}

    void vender_lanche(const std::string& lanche) {
        ++numero_;
        cozinha_.preparar_lanche(numero_, lanche);
        std::cout << "caixa: pedido " << numero_ << " entregue, proximo cliente\n";
    }

    void vender_bebida(const std::string& bebida) {
        ++numero_;
        bar_.preparar_bebida(numero_, bebida);
        std::cout << "caixa: pedido " << numero_ << " entregue, proximo cliente\n";
    }

private:
    Cozinha& cozinha_;
    Bar& bar_;
    int numero_ = 0;
};

int main() {
    Cozinha cozinha;
    Bar bar;
    Caixa caixa{cozinha, bar};
    caixa.vender_lanche("X-burguer");
    caixa.vender_bebida("suco de laranja");
    caixa.vender_lanche("misto quente");
}
