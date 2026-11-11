#include <iostream>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

// Evento: o que mudou num pedido
struct Aviso {
    int numero;
    std::string item;
    bool pronto;  // false: recusado
};

// Observador: contrato de quem quer ser avisado
class Observador {
public:
    virtual ~Observador() = default;
    virtual void receber(const Aviso& aviso) = 0;
};

// Sujeito (e receptor dos comandos): avisa a todos os inscritos, sem conhecê-los
class Cozinha {
public:
    explicit Cozinha(int paes) : paes_(paes) {}

    void assinar(Observador& observador) { observadores_.push_back(&observador); }

    std::string preparar(int numero, const std::string& item) {
        if (preparados_.count(numero) > 0) {
            return "repetido, ignorado";  // nada mudou: ninguém é avisado
        }
        if (paes_ == 0) {
            notificar(Aviso{numero, item, false});
            return "recusado, acabou o pao";
        }
        --paes_;
        preparados_.insert(numero);
        notificar(Aviso{numero, item, true});
        return "pronto (" + item + ")";
    }

    std::string repor_paes(int quantidade) {
        paes_ += quantidade;
        return "estoque com " + std::to_string(paes_) + " paes";
    }

private:
    void notificar(const Aviso& aviso) {
        for (Observador* observador : observadores_) {
            observador->receber(aviso);
        }
    }

    int paes_;
    std::set<int> preparados_;
    std::vector<Observador*> observadores_;  // emprestados: a cozinha não os destrói
};

// Observadores concretos: cada um decide como reagir
class Painel : public Observador {
public:
    void receber(const Aviso& aviso) override {
        if (aviso.pronto) {
            prontos_.push_back(aviso.numero);
            std::cout << "painel: PRONTO " << aviso.numero << '\n';
        }
    }
    const std::vector<int>& prontos() const { return prontos_; }

private:
    std::vector<int> prontos_;  // estado: o que está pronto agora
};

class Aplicativo : public Observador {
public:
    void receber(const Aviso& aviso) override {
        if (aviso.pronto) {
            std::cout << "app: pedido " << aviso.numero << " pronto, pode retirar\n";
        } else {
            std::cout << "app: pedido " << aviso.numero << " recusado, procure o caixa\n";
        }
    }
};

// Comando, comandos concretos e invocador: iguais aos de command.cpp
class Comando {
public:
    virtual ~Comando() = default;
    virtual std::string descrever() const = 0;
    virtual std::string executar() const = 0;
};

class PrepararPedido : public Comando {
public:
    PrepararPedido(Cozinha& cozinha, int numero, std::string item)
        : cozinha_(cozinha), numero_(numero), item_(std::move(item)) {}

    std::string descrever() const override { return "pedido " + std::to_string(numero_); }
    std::string executar() const override { return cozinha_.preparar(numero_, item_); }

private:
    Cozinha& cozinha_;
    int numero_;
    std::string item_;
};

class ReporPaes : public Comando {
public:
    ReporPaes(Cozinha& cozinha, int quantidade) : cozinha_(cozinha), quantidade_(quantidade) {}

    std::string descrever() const override {
        return "repor " + std::to_string(quantidade_) + " paes";
    }
    std::string executar() const override { return cozinha_.repor_paes(quantidade_); }

private:
    Cozinha& cozinha_;
    int quantidade_;
};

class Fila {
public:
    void receber(std::unique_ptr<Comando> comando) { pendentes_.push_back(std::move(comando)); }

    std::size_t pendentes() const { return pendentes_.size(); }

    void atender_todos() {
        for (const auto& comando : pendentes_) {
            historico_.push_back(comando->descrever() + ": " + comando->executar());
        }
        pendentes_.clear();
    }

    const std::vector<std::string>& historico() const { return historico_; }

private:
    std::vector<std::unique_ptr<Comando>> pendentes_;
    std::vector<std::string> historico_;
};

int main() {
    Painel painel;  // observadores criados antes da cozinha: vivem mais que ela
    Aplicativo app;
    Cozinha cozinha{2};
    cozinha.assinar(painel);
    cozinha.assinar(app);

    Fila fila;
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 1, "X-burguer"));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 2, "misto quente"));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 2, "misto quente"));  // reenvio
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 3, "X-salada"));
    fila.receber(std::make_unique<ReporPaes>(cozinha, 10));
    fila.receber(std::make_unique<PrepararPedido>(cozinha, 4, "X-burguer"));

    fila.atender_todos();
    std::cout << "historico da fila: " << fila.historico().size() << " comandas" << '\n';
    std::cout << "painel mostra:";
    for (int numero : painel.prontos()) {
        std::cout << ' ' << numero;
    }
    std::cout << '\n';
}
