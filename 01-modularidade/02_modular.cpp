#include <iostream>

class IFonteLeitura {
public:
    virtual ~IFonteLeitura() = default;
    virtual double valor() const = 0;
};

class FonteConstante : public IFonteLeitura {
    double percentual_;

public:
    explicit FonteConstante(double percentual) : percentual_(percentual) {}
    double valor() const override { return percentual_; }
};

class PoliticaAlarme {
    double limite_;

public:
    explicit PoliticaAlarme(double limite) : limite_(limite) {}
    bool aciona(double valor) const { return valor > limite_; }
};

class ControladorConsulta {
    const IFonteLeitura& fonte_;
    PoliticaAlarme politica_;

public:
    ControladorConsulta(const IFonteLeitura& fonte, PoliticaAlarme politica)
        : fonte_(fonte), politica_(politica) {}

    bool avaliar() const {
        return politica_.aciona(fonte_.valor());
    }
};

int main() {
    FonteConstante fonte{90};
    PoliticaAlarme politica{80};
    ControladorConsulta controlador{fonte, politica};
    const bool alerta = controlador.avaliar();
    std::cout << "LT-01: " << (alerta ? "ALERTA" : "NORMAL") << '\n';
}
