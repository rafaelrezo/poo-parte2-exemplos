#include <cassert>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Aquisicao {
    std::string sessao;
    int ciclo;
    double nivel;
};

class HistoricoMemoria {
    std::vector<Aquisicao> itens_;
public:
    bool salvar(const Aquisicao& aquisicao) {
        for (const auto& atual : itens_) {
            if (atual.sessao == aquisicao.sessao && atual.ciclo == aquisicao.ciclo) {
                if (atual.nivel != aquisicao.nivel) {
                    throw std::invalid_argument("identidade com conteudo diferente");
                }
                return false;
            }
        }
        itens_.push_back(aquisicao);
        return true;
    }
    std::vector<Aquisicao> listar() const { return itens_; }
};

int main() {
    HistoricoMemoria historico;
    const Aquisicao aquisicao{"ensaio", 1, 48.5};
    const bool nova = historico.salvar(aquisicao);
    const bool repetida = historico.salvar(aquisicao);
    assert(nova);
    assert(!repetida);
    assert(historico.listar().size() == 1);
    std::cout << "aquisicoes: " << historico.listar().size() << '\n';
}
