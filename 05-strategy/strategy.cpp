#include <cassert>
#include <iostream>

class PoliticaAlarme {
public:
    virtual ~PoliticaAlarme() = default;
    virtual bool aciona(double nivel) const = 0;
};

class NivelAlto : public PoliticaAlarme {
public:
    bool aciona(double nivel) const override { return nivel > 80; }
};

class ForaDaFaixa : public PoliticaAlarme {
public:
    bool aciona(double nivel) const override {
        return nivel < 20 || nivel > 80;
    }
};

class Monitor {
    const PoliticaAlarme& politica_;
public:
    explicit Monitor(const PoliticaAlarme& politica) : politica_(politica) {}
    bool avaliar(double nivel) const { return politica_.aciona(nivel); }
};

int main() {
    NivelAlto alto;
    ForaDaFaixa faixa;
    Monitor monitorAlto{alto};
    Monitor monitorFaixa{faixa};
    assert(!monitorAlto.avaliar(10));
    assert(monitorFaixa.avaliar(10));
    assert(!monitorAlto.avaliar(80));
    assert(!monitorFaixa.avaliar(80));
    std::cout << std::boolalpha;
    std::cout << "nivel 10: alto=" << monitorAlto.avaliar(10)
              << ", faixa=" << monitorFaixa.avaliar(10) << '\n';
}
