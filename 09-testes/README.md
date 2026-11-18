# 09. Testes e integração contínua

Este projeto mostra **onde fica o código**, **onde ficam os testes** e **qual
comando a CI repete**. É uma demonstração independente, não a solução do
trabalho da planta.

```text
09-testes/
├── src/
│   ├── cpp/
│   │   ├── medicao.hpp             regra de domínio
│   │   └── produtor_fixture.cpp    produtor JSON para teste de integração
│   └── planta/
│       ├── medicao.py              mesma regra em Python
│       ├── contrato.py             interpretação do JSON
│       ├── modelo.py               aquisição válida
│       ├── repository.py           persistência SQLite
│       ├── exportacao.py           CSV do histórico
│       └── painel.py               interface Streamlit
├── tests/
│   ├── cpp/teste_medicao.cpp       regras e fronteiras em C++
│   └── python/
│       ├── test_medicao.py         regras e fronteiras em Python
│       ├── test_integracao.py      processo C++ → consumidor Python
│       ├── test_referencia.py      SQLite real em pasta temporária
│       └── test_painel.py          interface com AppTest, sem servidor
└── Makefile                        contrato único de execução
```

Os testes importam o código de `src/`; o código de `src/` não importa os testes.
`build/` contém os executáveis gerados e está ignorada pelo Git.

## Executar localmente

Na raiz do repositório, crie um ambiente virtual e instale a dependência da
tela. Os outros testes usam apenas Python e C++ padrão.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make -C 09-testes test
```

O Make compila o teste C++ e o produtor JSON, executa `./build/teste_medicao`
e descobre os arquivos `tests/python/test_*.py` com `unittest`. Assim,
`test_integracao.py` sempre encontra o produtor já compilado. Um teste que
falha devolve código diferente de zero; o Make e o Actions param com falha.

Para observar cada lado separadamente:

```bash
make -C 09-testes test-cpp
make -C 09-testes test-python
```

`test-python` também compila o produtor C++ usado na integração. Para remover
os executáveis: `make -C 09-testes clean`.

## Como o GitHub Actions repete o teste

O arquivo [`.github/workflows/testes-exemplos.yml`](../.github/workflows/testes-exemplos.yml)
fica na raiz do repositório. Seu núcleo é:

```yaml
on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  testes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v7
        with:
          python-version: '3.12'
      - run: python -m pip install -r requirements.txt
      - run: make -C 09-testes test
```

No arquivo real, `paths` restringe a execução automática a mudanças nesta
pasta, no workflow ou em `requirements.txt`. `workflow_dispatch` permite
executá-lo manualmente na aba **Actions**. `contents: read` dá somente a
permissão necessária para ler o código. O job usa o **mesmo comando local**;
se a expectativa falhar, o status do commit mostrará falha e o log indicará
qual teste a produziu.

O fluxo didático é: branch → alteração em `src/` ou `tests/` → `make test` →
commit e push → Actions no mesmo commit → PR para a `main` do próprio fork.
Ao criar um fork, confira se os workflows estão habilitados na aba Actions.

Referências: [sintaxe de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
e [configurações do Actions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).
