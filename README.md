# Programas de referência — Parte 2

Demonstrações independentes das aulas. Não substituem arquivos do starter
poo-planta-controle e não implementam o trabalho completo nem suas extensões.
A pasta consulta-arquitetura acompanha a leitura opcional sobre arquitetura
hexagonal: um recorte do projeto público poo-estacionamento-hexagonal.

Para obter os programas e acompanhar atualizações:

git clone https://github.com/rafaelrezo/poo-parte2-exemplos.git
cd poo-parte2-exemplos
git pull    # nas aulas seguintes, para receber programas novos

Entre na pasta do tema escolhido. Para um programa C++:

g++ -std=c++17 -Wall -Wextra -Werror -pedantic NOME.cpp -o exemplo
./exemplo

Para Python: python3 NOME.py. Não use -DNDEBUG em C++ nem -O em Python nas
primeiras demonstrações, que utilizam assert. Os programas de console usam
a biblioteca padrão; a exceção são os programas C++ da pasta 04-contrato que
leem ou escrevem JSON, que usam nlohmann/json. Os comandos e as saídas
comentadas estão nas aulas.

A pasta 09-testes já contém as dependências das aulas 04 e 08. Nessa pasta:

g++ -std=c++17 -Wall -Wextra -Werror -pedantic teste_medicao.cpp -o teste_medicao
./teste_medicao
g++ -std=c++17 -Wall -Wextra -Werror -pedantic produtor_fixture.cpp -o produtor_fixture
python3 test_referencia.py
python3 test_integracao.py

Para o painel e test_painel.py, use ambiente virtual e instale requirements.txt
na raiz deste pacote. Depois: python3 test_painel.py (na pasta 09-testes).
AppTest não inicia um servidor de visualização. Para abrir a tela voluntariamente,
na pasta 08-repository: python3 -m streamlit run painel.py.
A demonstração repository.py usa banco temporário e não deixa um banco na pasta.
O teste test_painel.py prepara seus próprios dados e verifica a tela.

Na pasta 03-processos, os programas trocam dados por arquivos de texto
(nivel.txt, comando.txt, estado_bomba.txt) criados na própria pasta. A ordem de
execução e as saídas esperadas estão na aula 03.

A consulta TCP demonstra enquadramento por bytes, sem conexão ou servidor.
Fora da pasta 03-processos, os programas que escrevem em disco usam diretórios
temporários na demonstração.

Na pasta 04-contrato, os programas Python importam contrato.py e publicar.py
da mesma pasta. contrato.py também aceita um caminho:
python3 contrato.py aquisicao.json. Os programas C++ com JSON usam a biblioteca
nlohmann/json 3.11.3 (licença MIT), incluída em include/nlohmann:

g++ -std=c++17 -Wall -Wextra -Werror -pedantic -I ../include consumidor_nivel.cpp -o consumidor_nivel

Para o modelo, o consumidor e o painel em execução (dois terminais, na pasta
04-contrato, com o ambiente virtual ativado):

python3 modelo_nivel.py --ciclos 120 --intervalo 1
streamlit run painel_nivel.py
