#include <cassert>
#include <iostream>

enum class TipoAlarme { NivelAlto, ForaDaFaixa };

class Monitor {
    TipoAlarme tipo_;
public:
    explicit Monitor(TipoAlarme tipo) : tipo_(tipo) {}

    bool avaliar(double nivel) const {
        if (tipo_ == TipoAlarme::NivelAlto) {
            return nivel > 80;
        }
        return nivel < 20 || nivel > 80;
    }
};

int main() {
    Monitor monitorAlto{TipoAlarme::NivelAlto};
    Monitor monitorFaixa{TipoAlarme::ForaDaFaixa};
    assert(!monitorAlto.avaliar(10));
    assert(monitorFaixa.avaliar(10));
    assert(!monitorAlto.avaliar(80));
    assert(!monitorFaixa.avaliar(80));
    std::cout << std::boolalpha;
    std::cout << "nivel 10: alto=" << monitorAlto.avaliar(10)
              << ", faixa=" << monitorFaixa.avaliar(10) << '\n';
}
