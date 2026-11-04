#include <iostream>
#include <sstream>
#include <string>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

std::string ler_valor(const std::string& texto) {  // parsing + extração com diagnóstico
    try {
        const json documento = json::parse(texto);
        std::ostringstream saida;
        saida << "valor " << documento.at("valor").get<double>();
        return saida.str();
    } catch (const json::parse_error&) {
        return "parse_error: o texto não é um JSON completo";
    } catch (const json::out_of_range&) {
        return "out_of_range: o campo 'valor' não existe";
    } catch (const json::type_error&) {
        return "type_error: 'valor' não é número";
    }
}

int main() {
    const json leitura = {{"tag", "LT-01"}, {"tipo", "nivel"}, {"valor", 48.5},
                          {"unidade", "%"}, {"status", "operando"}, {"falha", nullptr}};

    const std::string texto = leitura.dump();  // serializar: objeto -> texto
    std::cout << "texto JSON: " << texto << '\n';

    const json lida = json::parse(texto);  // parsing: texto -> objeto json
    std::cout << "unidade: " << lida.at("unidade").get<std::string>() << '\n';
    std::cout << "falha é null? " << std::boolalpha << lida.at("falha").is_null() << '\n';

    std::cout << ler_valor(texto) << '\n';
    std::cout << ler_valor(R"({"tag": "LT-01", "valor": 48.5)") << '\n';
    std::cout << ler_valor(R"({"tag": "LT-01"})") << '\n';
    std::cout << ler_valor(R"({"valor": true})") << '\n';
    return 0;
}
