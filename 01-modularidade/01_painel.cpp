#include <iostream>

class SensorNivel {
public:
    double percentual = 90;
};

class PainelEstacao {
    SensorNivel sensor_;

public:
    void executar() const {
        const bool alerta = sensor_.percentual > 80;
        std::cout << "LT-01: " << (alerta ? "ALERTA" : "NORMAL") << '\n';
    }
};

int main() {
    PainelEstacao painel;
    painel.executar();
}
