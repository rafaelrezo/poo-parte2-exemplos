# Repository: clientes sem SQL

Compare `sem_repositorio.py` com `organizado-cpp/` e
`organizado-python/`. Os exemplos de histórico `repository.py` e
`painel.py` pertencem a outra demonstração da aula 08.

```text
Caixa e Relatorio ──> RepositorioPedidos (contrato)
                             ▲              ▲
                    Memoria ─┘              └─ SQLite (Python)
main ──> escolhe a implementação e monta os clientes
```

`Caixa` e `Relatorio` conhecem a entidade `Pedido` e o contrato, mas não
importam uma implementação concreta. C++ usa memória para mostrar o limite de
dependência. Python troca memória por SQLite no `main` e executa o mesmo
`test_contrato.py` nas duas implementações, além de testar o caixa sem banco.

Em `organizado-cpp/`, execute
`g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o repository
&& ./repository`. Em `organizado-python/`, execute `python3 main.py` e
`python3 test_contrato.py`. Os arquivos únicos antigos continuam para links
anteriores.
