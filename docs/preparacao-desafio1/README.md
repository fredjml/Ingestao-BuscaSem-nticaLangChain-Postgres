# Preparação — desafio1: Ingestão e Busca Semântica (LangChain + Postgres/pgVector)

> Pacote gerado conforme `docs/licoesaprendidas/` (kit canônico). **Somente documentação**: este pacote não contém nem autoriza código do desafio.
> Consolidação dos Passos 0–4 em sessão única feita **a pedido explícito do operador** (2026-09-04), mantendo separação por artefato. A Fase B (implementação) seguirá **um prompt por sessão**.

## Mapa Passo → artefato

| Passo | Artefato | Estado |
| --- | --- | --- |
| Contexto | [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | preenchido |
| 0 — Origem/estado | [00-MAPA-ORIGENS.md](00-MAPA-ORIGENS.md) | preenchido (fontes ausentes registradas) |
| 1 — Análise inicial | [01-ANALYSIS.md](01-ANALYSIS.md) | preenchido |
| 1.1 — Pre-flight | [02-PRE-FLIGHT.md](02-PRE-FLIGHT.md) | executado read-only em 2026-09-04 → **GO COM RISCOS** |
| 1.2 — Tools/MCP | [03-TOOLS.md](03-TOOLS.md) · [04-MCP.md](04-MCP.md) | preenchidos |
| 2 — Requisitos | [05-PRD.md](05-PRD.md) · [06-REQUIREMENTS.md](06-REQUIREMENTS.md) · [07-TRACEABILITY.md](07-TRACEABILITY.md) | preenchidos — **Gate 1 depende de DEC-01..08** |
| 3 — Arquitetura/segurança/evidência | [08-TDD.md](08-TDD.md) · [09-THREAT-MODEL.md](09-THREAT-MODEL.md) · [10-EVIDENCE-MANIFEST.md](10-EVIDENCE-MANIFEST.md) | preenchidos — **Gate 2 depende de DEC-01/05/06/07** |
| 4 — Plano/decisões | [11-IMPLEMENTATION-PLAN.md](11-IMPLEMENTATION-PLAN.md) · [12-DECISIONS.md](12-DECISIONS.md) | plano pronto; **8 decisões ABERTAS** |
| Prompts por Passo | [13-PROMPTS.md](13-PROMPTS.md) | pronto para Fase B/C/D |
| Infra de IA | [agents/](agents/) · [skills/desafio1-preparacao-implementacao/SKILL.md](skills/desafio1-preparacao-implementacao/SKILL.md) | 5 subagentes + skill adaptada |

## Autorização vigente

**Somente leitura + escrita nesta pasta.** Vetado: criar código do desafio, instalar software, executar serviços live, commit/push, uso de dado real. Autorizações futuras são **just-in-time por ação**.

## Bloqueios antes da Fase B (resumo)

~~DEC-01/02/03/07~~ — **todas as 9 decisões FECHADAS** em 2026-09-04 → Gates 1 e 2 fechados.

Restam apenas bloqueios de **ambiente** (Gate 0):

1. Instalar **Python 3.12** (com py launcher + pip) — autorização de infra necessária.
2. Iniciar o **Docker Desktop** (daemon parado).
3. Owner configura credenciais OpenAI e/ou Google no `.env` local (nunca no chat).
4. Reexecutar pre-flight → então fatia **A1** (clone do template), com autorização just-in-time.

Detalhes em [12-DECISIONS.md](12-DECISIONS.md) e [02-PRE-FLIGHT.md](02-PRE-FLIGHT.md).
