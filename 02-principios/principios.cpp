#include <cassert>
#include <iostream>
#include <stdexcept>
#include <string>

class ErroLeitura : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double ler() const = 0;  // °C; lança ErroLeitura se não medir
};

class SensorSimulado : public Sensor {
public:
    explicit SensorSimulado(double valor, bool disponivel = true)
        : valor_(valor), disponivel_(disponivel) {}

    double ler() const override {
        if (!disponivel_) {
            throw ErroLeitura("aquisição indisponível");
        }
        return valor_;
    }

private:
    double valor_;
    bool disponivel_;
};

class ControladorTemperatura {
public:
    ControladorTemperatura(const Sensor& sensor, double limite)
        : sensor_(sensor), limite_(limite) {}

    std::string decidir() const {
        return sensor_.ler() > limite_ ? "ligar resfriamento" : "manter";
    }

private:
    const Sensor& sensor_;
    double limite_;
};

int main() {
    // Fronteira da regra: abaixo, igual e acima do limite
    for (double valor : {89.0, 90.0, 91.0}) {
        SensorSimulado sensor(valor);
        ControladorTemperatura controlador(sensor, 90);
        const std::string esperado = valor > 90 ? "ligar resfriamento" : "manter";
        assert(controlador.decidir() == esperado);
    }

    // Falha de aquisição deve ser propagada, não convertida em decisão
    SensorSimulado ausente(0, false);
    ControladorTemperatura controlador(ausente, 90);
    bool falhou = false;
    try {
        controlador.decidir();
    } catch (const ErroLeitura&) {
        falhou = true;
    }
    assert(falhou);

    std::cout << "OK: abaixo, igualdade, acima e falha\n";
}
