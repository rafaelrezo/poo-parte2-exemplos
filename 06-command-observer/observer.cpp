#include <iostream>
#include <set>
#include <vector>

// Evento: o que aconteceu, com os dados que os interessados precisam
struct PedidoPronto {
    int numero;
};

// Observador: o contrato de quem quer ser avisado
class Observador {
public:
    virtual ~Observador() = default;
    virtual void receber(const PedidoPronto& evento) = 0;
};

// Sujeito: guarda os inscritos e os notifica, sem saber quem são
class Cozinha {
public:
    void assinar(Observador& observador) { observadores_.push_back(&observador); }

    void concluir(int numero) {
        if (prontos_.count(numero) > 0) {
            return;  // já estava pronto: nada mudou, nenhum evento
        }
        prontos_.insert(numero);
        std::cout << "cozinha: pedido " << numero << " pronto\n";
        for (Observador* observador : observadores_) {
            observador->receber(PedidoPronto{numero});
        }
    }

private:
    std::set<int> prontos_;                  // estado: pedidos já prontos
    std::vector<Observador*> observadores_;  // emprestados: a cozinha não os destrói
};

// Observadores concretos: cada um decide como reagir ao mesmo evento
class Painel : public Observador {
public:
    void receber(const PedidoPronto& evento) override {
        std::cout << "  painel: PRONTO " << evento.numero << '\n';
    }
};

class Aplicativo : public Observador {
public:
    void receber(const PedidoPronto& evento) override {
        std::cout << "  app: pedido " << evento.numero << " pronto, pode retirar\n";
    }
};

int main() {
    Painel painel;  // criados antes da cozinha: vivem mais que ela
    Aplicativo app;
    Cozinha cozinha;
    cozinha.assinar(painel);
    cozinha.assinar(app);

    cozinha.concluir(1);
    cozinha.concluir(2);
    std::cout << "(o cozinheiro aperta de novo o botao do pedido 2)\n";
    cozinha.concluir(2);
}
