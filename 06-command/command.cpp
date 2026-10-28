#include <cassert>
#include <iostream>
#include <stdexcept>
#include <vector>

struct Registro {
    int id;
    double nivel;
};

class LivroAuditoria {
    std::vector<Registro> registros_;
public:
    bool registrar(Registro registro) {
        if (registro.id <= 0) {
            throw std::invalid_argument("id deve ser positivo");
        }
        for (const auto& atual : registros_) {
            if (atual.id == registro.id) {
                if (atual.nivel != registro.nivel) {
                    throw std::invalid_argument("id repetido com outro conteudo");
                }
                return false;
            }
        }
        registros_.push_back(registro);
        return true;
    }
    std::size_t quantidade() const { return registros_.size(); }
};

class Comando {
public:
    virtual ~Comando() = default;
    virtual bool executar(LivroAuditoria& receptor) const = 0;
};

class RegistrarNivel : public Comando {
    Registro registro_;
public:
    explicit RegistrarNivel(Registro registro) : registro_(registro) {}
    bool executar(LivroAuditoria& receptor) const override {
        return receptor.registrar(registro_);
    }
};

class Executor {
public:
    bool executar(const Comando& comando, LivroAuditoria& receptor) const {
        return comando.executar(receptor);
    }
};

int main() {
    LivroAuditoria livro;
    RegistrarNivel comando{Registro{7, 48.5}};
    Executor executor;
    const bool primeiro = executor.executar(comando, livro);
    const bool repetido = executor.executar(comando, livro);
    assert(primeiro);
    assert(!repetido);
    assert(livro.quantidade() == 1);
    std::cout << "registros apos repetir: " << livro.quantidade() << '\n';
}
