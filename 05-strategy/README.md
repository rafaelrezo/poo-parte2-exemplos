# Strategy: frete como escolha isolada

Compare `sem_strategy.cpp` e `sem_strategy.py` com os projetos
`organizado-cpp/` e `organizado-python/`. Os arquivos únicos antigos
`strategy.*` continuam acessíveis por links anteriores.

```text
main (montagem) ──> modalidades concretas ──> Frete (contrato)
       │                                      ▲
       └──────────────> Pedido ───────────────┘
```

`Pedido` depende de `Frete`, não de `Retirada`, `PorPeso` ou `PorFaixa`.
A escolha da modalidade fica na montagem. Em Python,
`organizado-python/extensions/motoboy.py` acrescenta outra modalidade sem
modificar `lib/pedido.py`.

Execute `g++ -std=c++17 -Wall -Wextra -Werror -pedantic main.cpp -o strategy
&& ./strategy` em `organizado-cpp/`. Execute `python3 main.py` e
`python3 -m extensions.motoboy` em `organizado-python/`.
