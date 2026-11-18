#pragma once

#include "comando.hpp"
#include <memory>
#include <string>
#include <utility>
#include <vector>

class Fila {
public:
    void receber(std::unique_ptr<Comando> comando) { pendentes_.push_back(std::move(comando)); }

    std::size_t pendentes() const { return pendentes_.size(); }

    void atender_todos() {
        for (const auto& comando : pendentes_) {
            comando->executar();
            historico_.push_back(comando->descrever());
        }
        pendentes_.clear();
    }

    const std::vector<std::string>& historico() const { return historico_; }

private:
    std::vector<std::unique_ptr<Comando>> pendentes_;
    std::vector<std::string> historico_;
};
