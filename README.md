# Repositório agêntico (Tiger, Turtle, Termite)

Fluxo: **Tiger** (histórias funcionais) -> revisão humana -> **Turtle** (tech spec + branches) -> revisão humana -> **Termite** (Plan -> Code TDD -> Verify) -> graphify manual -> done.

## Como iniciar uma demanda
1. Copie `artifacts/active/_example-story/` para `artifacts/active/<slug>/` e ajuste `demand-context.json` (valide contra `schemas/demand-context.schema.json`).
2. Invoque o agente Tiger (skill `agent-tiger-product`).
3. Após cada etapa, revise e registre a aprovação em `approvals[]`.

## Como adicionar um repositório
Clone dentro de `repos/<nome>/` (cada pasta é um repo git independente, ignorado pelo git deste repositório). Cada repo recebe o graphify em `knowledge/repositories/<nome>/graphify-out/`, gerado manualmente.

## Instalar o RTK em uma máquina nova
Windows: `winget install rtk-ai.rtk`; macOS/Linux: `brew install rtk`. Verifique com `rtk gain`. Nunca use `cargo install rtk`. Detalhes em `docs/research/rtk-setup.md`. Sem o RTK o hook não falha: os comandos rodam normalmente.

## Status das fases
- Fase 1 (fundação, esqueleto, contratos): concluída
- Fase 2 (conteúdo de agentes, guides e templates): pendente
