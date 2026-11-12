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
a biblioteca padrão; a exceção são os programas C++ da pasta
04-dispositivo-painel que escrevem JSON, que usam nlohmann/json. Os comandos e
as saídas comentadas estão nas aulas.

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
Fora das pastas 03-processos e 07-banco-de-dados, os programas que escrevem em
disco usam diretórios temporários ou bancos em memória na demonstração.

A pasta 04-dispositivo-painel acompanha o guia prático da aula 04. Cada
subpasta passo-N contém o estado do projeto ao final daquele passo, para
comparação; o estudante constrói o projeto na própria pasta. Os programas C++
com JSON usam nlohmann/json 3.11.3 (licença MIT), incluída em include/nlohmann.
Dentro de uma subpasta passo-N:

g++ -std=c++17 -Wall -Wextra -Werror -pedantic -I ../../include dispositivo.cpp -o dispositivo

No passo 7, dois processos trocam serie_nivel.json (o painel com o ambiente
virtual ativado):

./dispositivo 300 1000
streamlit run painel.py

Na pasta `05-strategy`, compare `sem_strategy.cpp` e `sem_strategy.py` com
`strategy.cpp` e `strategy.py`: o mesmo cálculo de frete, antes e depois do padrão.
`motoboy.py` acrescenta uma modalidade sem modificar `strategy.py`.

Na pasta `06-command-observer`, cada padrão tem seu par antes/depois:
`sem_command.*` → `command.*` (o caixa entrega comandas a uma fila, que atende
cozinha e bar sem conhecê-los) e `sem_observer.*` → `observer.*` (a cozinha avisa
painel e aplicativo sem conhecê-los). `sobremesa.py` acrescenta um setor sem
modificar `command.py`; `contador.py` inscreve um observador novo sem modificar
`observer.py`.

Na pasta `07-banco-de-dados`, os programas seguem o percurso da aula 07:
`pedidos_lista.py` (os pedidos somem ao terminar) → `pedidos_json.py` (persiste,
mas duplica ao executar de novo) → `pedidos_sqlite.py` (chave primária, consultas
e parâmetros `?`) → `transacao.py` (tudo ou nada). Execute os dois do meio duas
vezes. Eles criam `pedidos.json` e `lanchonete.db` na própria pasta; apague esses
arquivos para recomeçar.

Na pasta `08-repository`, compare `sem_repositorio.py` com `repositorio.py` e
`repositorio.cpp`: o caixa e o relatório da lanchonete antes e depois do padrão.
`teste_repositorio.py` testa as duas implementações com o mesmo teste de contrato
e o caixa sem banco, sem modificar `repositorio.py`. `repository.py` e `painel.py`
são o histórico de aquisições do trabalho, usados também na pasta `09-testes`.
