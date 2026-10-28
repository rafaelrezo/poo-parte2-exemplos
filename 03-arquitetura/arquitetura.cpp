#include <iostream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>

// ---------- Núcleo: regra, portas e caso de uso. Nenhuma E/S aqui. ----------

class Tarifa {  // regra do negócio; varia por Strategy (aula 05)
public:
    virtual ~Tarifa() = default;
    virtual int calcular(int minutos) const = 0;
};

class TarifaPorHora : public Tarifa {  // 15 min grátis; R$ 8,00 por hora iniciada
public:
    int calcular(int minutos) const override {
        if (minutos <= 15) {
            return 0;
        }
        return ((minutos + 59) / 60) * 800;
    }
};

class Relogio {  // porta de saída: o núcleo precisa saber a hora
public:
    virtual ~Relogio() = default;
    virtual int agora_em_minutos() const = 0;
};

class RepositorioEntradas {  // porta de saída: o núcleo precisa lembrar entradas
public:
    virtual ~RepositorioEntradas() = default;
    virtual void guardar(const std::string& placa, int minuto) = 0;
    virtual std::optional<int> retirar(const std::string& placa) = 0;
};

class ServicoEstacionamento {  // porta de entrada: suas operações são os casos de uso
public:
    ServicoEstacionamento(const Tarifa& tarifa, RepositorioEntradas& entradas,
                          const Relogio& relogio)
        : tarifa_(tarifa), entradas_(entradas), relogio_(relogio) {}

    void registrar_entrada(const std::string& placa) {
        entradas_.guardar(placa, relogio_.agora_em_minutos());
    }

    int registrar_saida(const std::string& placa) {  // devolve o valor em centavos
        const std::optional<int> entrada = entradas_.retirar(placa);
        if (!entrada) {
            throw std::runtime_error("não há entrada aberta para " + placa);
        }
        return tarifa_.calcular(relogio_.agora_em_minutos() - *entrada);
    }

private:
    const Tarifa& tarifa_;
    RepositorioEntradas& entradas_;
    const Relogio& relogio_;
};

// ---------- Adaptadores de saída: implementam as portas com uma tecnologia ----------

class RelogioSimulado : public Relogio {
public:
    explicit RelogioSimulado(int inicio) : agora_(inicio) {}
    int agora_em_minutos() const override { return agora_; }
    void avancar(int minutos) { agora_ += minutos; }

private:
    int agora_;
};

class EntradasEmMemoria : public RepositorioEntradas {
public:
    void guardar(const std::string& placa, int minuto) override { entradas_[placa] = minuto; }

    std::optional<int> retirar(const std::string& placa) override {
        const auto encontrada = entradas_.find(placa);
        if (encontrada == entradas_.end()) {
            return std::nullopt;
        }
        const int minuto = encontrada->second;
        entradas_.erase(encontrada);
        return minuto;
    }

private:
    std::map<std::string, int> entradas_;
};

// ---------- Montagem e adaptador de entrada: o único trecho que conhece tudo ----------

int main() {
    TarifaPorHora tarifa;
    EntradasEmMemoria entradas;
    RelogioSimulado relogio(8 * 60);  // 08:00
    ServicoEstacionamento servico(tarifa, entradas, relogio);

    servico.registrar_entrada("ABC1D23");
    servico.registrar_entrada("XYZ9876");
    relogio.avancar(10);
    std::cout << "XYZ9876 pagou " << servico.registrar_saida("XYZ9876") << " centavos\n";
    relogio.avancar(85);
    std::cout << "ABC1D23 pagou " << servico.registrar_saida("ABC1D23") << " centavos\n";
    try {
        servico.registrar_saida("ABC1D23");
    } catch (const std::runtime_error& erro) {
        std::cout << "erro: " << erro.what() << '\n';
    }
    return 0;
}
