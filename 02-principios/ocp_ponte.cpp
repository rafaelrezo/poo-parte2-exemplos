#include <iostream>

class PoliticaAlarme {  // equivale à ABC do Python
public:
    virtual ~PoliticaAlarme() = default;
    virtual bool aciona(double temperatura) const = 0;  // equivale a @abstractmethod
};

class AlarmeMaximo : public PoliticaAlarme {
public:
    explicit AlarmeMaximo(double maximo) : maximo_(maximo) {}
    bool aciona(double temperatura) const override { return temperatura > maximo_; }

private:
    double maximo_;
};

class AlarmeFaixa : public PoliticaAlarme {
public:
    AlarmeFaixa(double minimo, double maximo) : minimo_(minimo), maximo_(maximo) {}
    bool aciona(double temperatura) const override {
        return temperatura < minimo_ || temperatura > maximo_;
    }

private:
    double minimo_;
    double maximo_;
};

class ControladorAlarme {  // composição: guarda uma referência ao contrato
public:
    explicit ControladorAlarme(const PoliticaAlarme& politica) : politica_(politica) {}
    bool avaliar(double temperatura) const { return politica_.aciona(temperatura); }

private:
    const PoliticaAlarme& politica_;
};

int main() {
    AlarmeMaximo maximo(90);
    AlarmeFaixa faixa(20, 90);
    ControladorAlarme com_maximo(maximo);
    ControladorAlarme com_faixa(faixa);

    std::cout << std::boolalpha;
    std::cout << "máximo 90, 15 °C -> " << com_maximo.avaliar(15) << '\n';
    std::cout << "faixa 20–90, 15 °C -> " << com_faixa.avaliar(15) << '\n';
}
