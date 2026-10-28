#include <cassert>
#include <iostream>
#include <string>
#include <vector>

struct EventoAlarme {
    bool ativo;
};

class Observador {
public:
    virtual ~Observador() = default;
    virtual void receber(const EventoAlarme& evento) = 0;
};

class Registro : public Observador {
    std::vector<std::string> mensagens_;
public:
    void receber(const EventoAlarme& evento) override {
        mensagens_.push_back(evento.ativo ? "ATIVOU" : "NORMALIZOU");
    }
    const std::vector<std::string>& mensagens() const { return mensagens_; }
};

class Contador : public Observador {
    int quantidade_ = 0;
public:
    void receber(const EventoAlarme&) override { ++quantidade_; }
    int quantidade() const { return quantidade_; }
};

class MonitorNivel {
    bool ativo_ = false;
    std::vector<Observador*> observadores_;
public:
    void assinar(Observador& observador) {
        for (auto* atual : observadores_) {
            if (atual == &observador) {
                return;
            }
        }
        observadores_.push_back(&observador);
    }
    void avaliar(double nivel) {
        const bool novo = nivel > 80;
        if (novo == ativo_) {
            return;
        }
        ativo_ = novo;
        for (auto* observador : observadores_) {
            observador->receber(EventoAlarme{ativo_});
        }
    }
};

int main() {
    Registro registro;
    Contador contador;
    MonitorNivel monitor;
    monitor.assinar(registro);
    monitor.assinar(contador);
    monitor.assinar(contador);
    for (double nivel : {79.0, 81.0, 82.0, 80.0}) {
        monitor.avaliar(nivel);
    }
    assert(contador.quantidade() == 2);
    for (const auto& mensagem : registro.mensagens()) {
        std::cout << mensagem << '\n';
    }
    std::cout << "transicoes: " << contador.quantidade() << '\n';
}
