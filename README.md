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

A pasta [09-testes](09-testes/README.md) separa `src/` de `tests/` e possui um
`Makefile` com o comando único `make -C 09-testes test`. O mesmo comando roda em
[`.github/workflows/testes-exemplos.yml`](.github/workflows/testes-exemplos.yml)
após push ou PR que altere os exemplos de testes. Instale `requirements.txt`
em um ambiente virtual para incluir o Streamlit usado por `test_painel.py`.
AppTest verifica a tela sem iniciar um servidor de visualização.

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

## Padrões como pequenos projetos

As versões `sem_*` mantêm o problema visível em um arquivo. As versões principais
com Strategy, Command, Observer e Repository agora são projetos independentes.
Em C++, `lib/` contém contratos e classes em cabeçalhos curtos; `main.cpp` apenas
monta e usa os objetos. Em Python, `lib/` é um pacote; `main.py` faz a montagem.
As extensões Python ficam em `extensions/`. Os arquivos únicos antigos com o
padrão permanecem para links anteriores, mas o percurso principal é o projeto.

| Padrão | Projeto C++ | Projeto Python | O cliente conhece |
|---|---|---|---|
| Strategy | `05-strategy/organizado-cpp` | `05-strategy/organizado-python` | `Frete`, não a modalidade concreta |
| Command | `06-command-observer/command-cpp` | `06-command-observer/command-python` | `Comando`, não cozinha ou bar |
| Observer | `06-command-observer/observer-cpp` | `06-command-observer/observer-python` | `Observador`, não painel ou aplicativo |
| Repository | `08-repository/organizado-cpp` | `08-repository/organizado-python` | `RepositorioPedidos`, não memória ou SQLite |

Estrutura que se repete nos exemplos organizados:

```text
organizado-cpp/                 organizado-python/
├── lib/  (contrato e classes)  ├── lib/  (contrato e módulos)
└── main.cpp  (montagem)        ├── main.py  (montagem)
                                └── extensions/ ou test_contrato.py
```

A pasta sozinha não desacopla o código: veja os imports de `Pedido`, `Fila`,
`Cozinha`, `Caixa` e `Relatorio`. Eles dependem do contrato; `main` escolhe
implementações concretas e liga os objetos. As demonstrações são independentes
do projeto avaliado e não contêm soluções de suas extensões.

### 05. Strategy

Compare `05-strategy/sem_strategy.cpp` e `sem_strategy.py` com os projetos
`organizado-cpp` e `organizado-python`. Em `lib/`, o contrato `Frete`, as
modalidades e `Pedido` ficam em arquivos distintos. A montagem escolhe a
modalidade fora do pedido. Execute a partir da raiz deste repositório:

```bash
cd 05-strategy/organizado-cpp
g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o strategy
./strategy
cd ../organizado-python
python3 main.py
python3 -m extensions.motoboy
cd ../..
```

`extensions/motoboy.py` acrescenta uma modalidade sem editar `lib/pedido.py`.

### 06. Command e Observer

Command e Observer ficam em **projetos diferentes** dentro de
`06-command-observer/`. Compare antes cada `sem_command.*` ou
`sem_observer.*`. A fila importa somente `Comando`; a cozinha importa somente
`Observador`. Execute, em cada pasta, o `main` da linguagem:

```bash
cd 06-command-observer/command-cpp
g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o command
./command
cd ../command-python
python3 main.py
python3 -m extensions.sobremesa
cd ../observer-cpp
g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o observer
./observer
cd ../observer-python
python3 main.py
python3 -m extensions.contador
cd ../..
```

`sobremesa` acrescenta receptor e comando sem alterar a fila; `contador`
acrescenta um observador sem alterar a cozinha.

### 07. Banco de dados

Na pasta `07-banco-de-dados`, os programas seguem lista → JSON → SQLite →
transação. `pedidos_json.py` e `pedidos_sqlite.py` criam arquivos na própria
pasta; execute duas vezes para ver a diferença e apague os arquivos para
recomeçar.

### 08. Repository

Compare `08-repository/sem_repositorio.py` com os projetos
`organizado-cpp` e `organizado-python`. `lib/` separa entidade, contrato,
armazenamentos e clientes. Em Python, o mesmo teste de contrato roda com
memória e SQLite; `Caixa` é testado sem banco:

```bash
cd 08-repository/organizado-cpp
g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o repository
./repository
cd ../organizado-python
python3 main.py
python3 test_contrato.py
cd ../..
```

`08-repository/repository.py` e `painel.py` são outra demonstração, do histórico
de aquisições do trabalho. `09-testes/src/planta/` mantém uma cópia independente
para mostrar os testes sem depender de outra pasta. Os arquivos únicos
`repositorio.cpp`, `repositorio.py` e `teste_repositorio.py` continuam disponíveis
para links anteriores.

Em todos os projetos, execute os comandos **dentro da pasta indicada**.
Os programas C++ organizados usam cabeçalhos didáticos em `lib/` e não exigem
instalação de uma biblioteca externa. Para testar o efeito do desacoplamento,
identifique qual arquivo mudaria ao acrescentar uma implementação concreta
e quais clientes permaneceriam iguais.
