#include <iostream>

class PoliticaAlarme {
    double limite_;  // nível que aciona o alarme
    double margem_;  // zona morta para evitar alarmes repetidos

public:
    PoliticaAlarme(double limite, double margem)
        : limite_(limite), margem_(margem) {}

    bool aciona(double nivel) const { return nivel > limite_; }
};

struct LeituraNivelPercentual {
    double valor;
};

class PoliticaAlarmeSegura {
    double limite_;
    double margem_;

public:
    PoliticaAlarmeSegura(double limite, double margem)
        : limite_(limite), margem_(margem) {}

    bool aciona(LeituraNivelPercentual leitura) const {
        return leitura.valor > limite_;
    }
};

int main() {
    double nivel = 30.0; // nivel moderado — não deveria gerar alarme

    // Intenção: limite=80%, margem=5%
    // Dúvida natural: qual parâmetro vem primeiro?
    PoliticaAlarme correta{80, 5};    // correto
    PoliticaAlarme invertida{5, 80};  // limite e margem trocados

    std::cout << "Nivel 30% — correta   (limite=80, margem=5): "
              << (correta.aciona(nivel) ? "ALERTA" : "NORMAL") << '\n';
    std::cout << "Nivel 30% — invertida (limite=5, margem=80): "
              << (invertida.aciona(nivel) ? "ALERTA" : "NORMAL") << '\n';

    // Solução: nomear o papel de cada valor
    LeituraNivelPercentual leitura{30};
    PoliticaAlarmeSegura segura{80, 5};
    std::cout << "Com tipo nomeado              : "
              << (segura.aciona(leitura) ? "ALERTA" : "NORMAL") << '\n';
}
