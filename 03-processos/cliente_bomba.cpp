#include <fstream>
#include <iostream>
#include <string>
#include <utility>

enum class Situacao { pendente, confirmado, recusado };

class ClienteBomba {
public:
    ClienteBomba(std::string arquivo_comando, std::string arquivo_estado)
        : arquivo_comando_(std::move(arquivo_comando)),
          arquivo_estado_(std::move(arquivo_estado)) {}

    void pedir_ligar(int id) {  // grava o pedido; não liga nada
        std::ofstream arquivo(arquivo_comando_);
        arquivo << "id " << id << "\nbomba ligar\n";
    }

    Situacao conferir(int id) {  // compara a resposta do painel com o pedido
        std::ifstream arquivo(arquivo_estado_);
        std::string chave_id;
        std::string chave_bomba;
        std::string estado;
        std::string chave_motivo;
        int ultimo = 0;
        arquivo >> chave_id >> ultimo >> chave_bomba >> estado >> chave_motivo >> motivo_;
        if (!arquivo || ultimo != id) {
            return Situacao::pendente;
        }
        return estado == "ligada" ? Situacao::confirmado : Situacao::recusado;
    }

    const std::string& motivo() const { return motivo_; }

private:
    std::string arquivo_comando_;
    std::string arquivo_estado_;
    std::string motivo_;
};

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "uso: ./cliente_bomba pedir|conferir ID\n";
        return 2;
    }
    const std::string operacao = argv[1];
    const int id = std::stoi(argv[2]);
    ClienteBomba cliente("comando.txt", "estado_bomba.txt");

    if (operacao == "pedir") {
        cliente.pedir_ligar(id);
        std::cout << "pedido " << id << " gravado em comando.txt\n";
        return 0;
    }
    switch (cliente.conferir(id)) {
    case Situacao::pendente:
        std::cout << "pedido " << id << ": sem resposta do painel\n";
        break;
    case Situacao::confirmado:
        std::cout << "pedido " << id << ": confirmado, bomba ligada\n";
        break;
    case Situacao::recusado:
        std::cout << "pedido " << id << ": recusado (" << cliente.motivo() << ")\n";
        break;
    }
    return 0;
}
