# Split de histórias em partes (backend / frontend)

Decisão de 2026-11-18. Uma história grande, como `login-register`, pode ser dividida em **partes** desenvolvidas em sequência, cada uma com o fluxo completo (Tiger -> Turtle -> Termite), dentro do **mesmo workspace**.

## Estrutura

```
artifacts/active/<slug>/
├── 00-split.md                 escopo de cada parte, ordem, contrato e riscos
├── delivery/  design/          coleta e referências comuns às partes (sem demand-context.json)
├── <parte-1>/{delivery,design,demand-context.json}
└── <parte-2>/{delivery,design,demand-context.json}
```

## Regras

- **Referência:** os comandos aceitam `<slug>` (demanda única) ou `<slug>/<parte>`, por exemplo `/tiger login-register/backend`.
- **Uma demanda por parte:** cada parte tem seu `demand-context.json`, status, aprovações, branches e graphify próprios. O `slug` é o do workspace; o schema ganhou `part` e `dependsOn`.
- **Ordem:** `dependsOn` lista as partes que precisam estar `done` ou `archived`. Tiger (intake) e Turtle recusam se alguma ainda estiver aberta.
- **Entrada da parte seguinte:** o Tiger da segunda parte recebe o `02-tech-spec.md` da primeira como entrada (contrato real).
- **Escopo:** o `00-split.md` limita o que cada parte entrega. O Tiger da parte herda só o escopo dela.
- **Branches:** `<tipo>/<slug>-<parte>`, por exemplo `feat/login-register-backend`.
- **demandType:** cada parte tem o seu (`backend`, `frontend`...). `fullstack` fica para demandas únicas.
- **Arquivamento:** ao fechar uma parte, `active/<slug>/<parte>` vai para `archive/<slug>/<parte>`. Os arquivos da raiz do workspace só migram quando a última parte fecha.
- **Quando dividir:** demanda `fullstack` em que backend e frontend entregam valor em separado e o frontend depende do contrato do backend. O Tiger recomenda o split (padrão: dividir) e o humano decide.

## Criar um split

1. Crie `artifacts/active/<slug>/` com a coleta e o `00-split.md` (modelo em `knowledge/templates/template-split.md`).
2. Rode `/tiger <slug>/<parte-1>`. O Tiger cria as pastas da parte no intake. Ao fechar a parte 1, rode `/tiger <slug>/<parte-2>`.
