# Command e Observer: projetos separados

Os arquivos `sem_command.*` e `sem_observer.*` mostram o acoplamento inicial.
Cada solução tem projeto C++ e Python próprio, com `lib/` para contratos e
colaboradores e `main` para a montagem.

```text
Command:  caixa → Comando → receptor    Fila → Comando
Observer: Cozinha → Observador ← Painel / Aplicativo
```

No Command, `Fila` importa apenas `Comando`; ela não importa cozinha nem bar.
No Observer, `Cozinha` importa apenas `Observador`; ela não importa painel
nem aplicativo. As extensões Python demonstram a adição de sobremesa e contador
sem alterar esses clientes. Os arquivos únicos antigos permanecem para links
anteriores.

Em `command-cpp/` e `observer-cpp/`, compile `main.cpp` com
`g++ -std=c++17 -Wall -Wextra -Werror -pedantic`. Em `command-python/` e
`observer-python/`, execute `python3 main.py`. Para as extensões, execute
`python3 -m extensions.sobremesa` ou
`python3 -m extensions.contador` na pasta Python correspondente.
