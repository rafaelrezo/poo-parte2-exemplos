#include <chrono>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>

using std::chrono::system_clock;

std::string para_texto(system_clock::time_point instante) {  // ISO 8601 em UTC
    const std::time_t segundos = system_clock::to_time_t(instante);
    const std::tm utc = *std::gmtime(&segundos);
    std::ostringstream saida;
    saida << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return saida.str();
}

int main() {
    // 1. Relógio de parede: o instante de agora (muda a cada execução)
    std::cout << "agora, em UTC:       " << para_texto(system_clock::now()) << '\n';

    // 2. Um instante guardado como segundos desde 1970 e escrito como texto
    const system_clock::time_point ocorrencia = system_clock::from_time_t(1792605600);
    std::cout << "1792605600 s em UTC: " << para_texto(ocorrencia) << '\n';

    // 3. Diferença entre dois instantes
    const auto recebimento = ocorrencia + std::chrono::seconds(3);
    const auto atraso = std::chrono::duration_cast<std::chrono::seconds>(recebimento - ocorrencia);
    std::cout << "recebida às " << para_texto(recebimento) << " -> atraso de "
              << atraso.count() << " s\n";

    // 4. Duração dentro do programa: relógio monotônico
    const auto inicio = std::chrono::steady_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    const auto passou = std::chrono::steady_clock::now() - inicio;
    std::cout << "duração medida:      " << std::fixed << std::setprecision(1)
              << std::chrono::duration<double>(passou).count() << " s\n";
    return 0;
}
