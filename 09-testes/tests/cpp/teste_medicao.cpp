#include "medicao.hpp"
#include <iostream>
#include <stdexcept>
#include <string>

void exigir(bool condicao, const std::string& mensagem) {
    if (!condicao) {
        throw std::runtime_error(mensagem);
    }
}

int main() {
    try {
        Medicao medicao{50};
        exigir(medicao.valor() == 50, "construtor perdeu o valor inicial");
        exigir(medicao.atualizar(0), "fronteira 0 deveria ser aceita");
        exigir(medicao.atualizar(100), "fronteira 100 deveria ser aceita");
        exigir(!medicao.atualizar(-1), "valor negativo deveria ser recusado");
        exigir(!medicao.atualizar(101), "valor acima de 100 deveria ser recusado");
        exigir(medicao.valor() == 100, "recusa alterou o ultimo valor valido");
        bool rejeitou = false;
        try {
            Medicao invalida{-1};
        } catch (const std::invalid_argument&) {
            rejeitou = true;
        }
        exigir(rejeitou, "construtor aceitou estado invalido");
        std::cout << "OK: construcao, fronteiras e preservacao de estado\n";
        return 0;
    } catch (const std::exception& erro) {
        std::cerr << "FALHOU: " << erro.what() << '\n';
        return 1;
    }
}
