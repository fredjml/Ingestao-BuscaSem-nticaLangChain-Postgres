---
name: desafio1-preparacao-implementacao
description: Prepara — sem alterar código — o desafio1 (Ingestão e Busca Semântica com LangChain + Postgres/pgVector) para implementação. Executa os Passos 0 a 4 do kit docs/licoesaprendidas/ (origem, pre-flight, requisitos, arquitetura/segurança/evidência, plano incremental e decisões). Usar quando o operador pedir preparação, análise, requisitos ou planejamento do desafio1. NÃO usar para implementar código (isso é o Passo 5, com autorização just-in-time por fatia).
---

# desafio1 — Preparação para implementação

Orquestra os Passos 0–4 do kit canônico para o desafio1, produzindo/atualizando o pacote em `docs/preparacao-desafio1/`.

## Autorização

SOMENTE LEITURA do workspace + escrita exclusiva em `docs/preparacao-desafio1/`. Vetado: código do desafio, instalação, serviços live, commit/push, dado real, valores de segredo.

## Sequência (um Passo por sessão)

1. **Passo 0** → `00-MAPA-ORIGENS.md`: fontes com precedência, baseline datada, inconsistências INC-xx (não decidir conflito — registrar).
2. **Passo 1.1** → `02-PRE-FLIGHT.md` (subagente `analyst-preflight`): comandos read-only; veredito GO/GO COM RISCOS/NO-GO; software a instalar.
3. **Passo 1.2** → `03-TOOLS.md` + `04-MCP.md`: ferramentas por requisito/risco/licença/telemetria/fallback.
4. **Passo 2** → `06-REQUIREMENTS.md` + `07-TRACEABILITY.md` (subagente `requirements-engineer`) e `05-PRD.md`: requisitos atômicos Dado/Quando/Então; Gate 1.
5. **Passo 3** → `08-TDD.md`, `09-THREAT-MODEL.md` (`security-architect`), `10-EVIDENCE-MANIFEST.md` (`evidence-planner`); Gate 2.
6. **Passo 4** → `11-IMPLEMENTATION-PLAN.md` (`plan-decomposer`) + `12-DECISIONS.md`: fatias reversíveis com teste focal; decisões DEC-xx com owner; DoR.

## Princípios vinculados (do kit)

Fonte primária vence derivado; fato ≠ inferência ≠ hipótese ≠ decisão; mock ≠ live ≠ UI; autorização just-in-time por ação; sem segredo/PII em logs; 2 falhas iguais sem nova hipótese → escalar (`licoesaprendidas/10-escalonamento.md`); "não foi possível determinar" é válido.

## Bloqueios conhecidos (2026-09-04)

DEC-01 (provider), DEC-02 (template × scaffold), DEC-03 (PDF), DEC-07 (compliance de envio a API externa) + instalação de Python e daemon Docker. Não avançar ao Passo 5 com bloqueio aberto.

## Critério de parada

Gate 0/1/2 não fecha; fonte primária ausente; escopo expande além da preparação; suspeita de segredo → parar, registrar e escalar ao owner.
