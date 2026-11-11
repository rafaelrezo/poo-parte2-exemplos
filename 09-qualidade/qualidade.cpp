#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

struct EstadoRecebido {
    bool disponivel;
    double idadeSegundos;
    bool alarmeAtivo;
};

enum class Situacao { Indisponivel, Obsoleto, Alarme, Normal };

Situacao classificar(const EstadoRecebido& estado) {
    if (!estado.disponivel) {
        return Situacao::Indisponivel;
    }
    if (!std::isfinite(estado.idadeSegundos) || estado.idadeSegundos < 0) {
        throw std::invalid_argument("idade invalida");
    }
    if (estado.idadeSegundos > 5) {
        return Situacao::Obsoleto;
    }
    if (estado.alarmeAtivo) {
        return Situacao::Alarme;
    }
    return Situacao::Normal;
}

std::string texto(Situacao situacao) {
    switch (situacao) {
        case Situacao::Indisponivel: return "INDISPONIVEL";
        case Situacao::Obsoleto: return "OBSOLETO";
        case Situacao::Alarme: return "ALARME";
        case Situacao::Normal: return "NORMAL";
    }
    throw std::logic_error("situacao desconhecida");
}

int main() {
    assert(classificar({true, 5, false}) == Situacao::Normal);
    assert(classificar({true, 5, true}) == Situacao::Alarme);
    assert(classificar({true, 6, true}) == Situacao::Obsoleto);
    assert(classificar({false, 0, false}) == Situacao::Indisponivel);
    for (const auto& estado : {EstadoRecebido{true, 5, false},
                               EstadoRecebido{true, 5, true},
                               EstadoRecebido{true, 6, true},
                               EstadoRecebido{false, 0, false}}) {
        std::cout << texto(classificar(estado)) << '\n';
    }
}
