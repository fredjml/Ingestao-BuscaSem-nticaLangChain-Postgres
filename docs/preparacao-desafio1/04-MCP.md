# 04 — Inventário MCP / agentes de IA (desafio1)

Data: 2026-09-04.

## 1. MCP servers

| MCP | Necessário? | Justificativa |
| --- | --- | --- |
| Nenhum | — | O desafio é local: Postgres em Docker + APIs OpenAI/Google via SDK. Nenhum MCP é requisito. |
| (opcional) MCP Postgres | não recomendado neste ciclo | inspeção do banco pode ser feita com `docker exec … psql` read-only; MCP aumenta superfície de risco sem ganho material |

Regra do kit: MCP configurado não prova descoberta, autenticação, saúde ou autorização. Se algum MCP for proposto depois, exige auditoria de `licoesaprendidas/04-ia-rules-skills-tools-mcp-agents.md` e autorização do owner.

## 2. Infra de IA deste pacote (subagentes + skill)

Definidos nesta pasta:

- [agents/analyst-preflight.md](agents/analyst-preflight.md) — pre-flight read-only
- [agents/requirements-engineer.md](agents/requirements-engineer.md) — requisitos/rastreabilidade
- [agents/security-architect.md](agents/security-architect.md) — threat model
- [agents/evidence-planner.md](agents/evidence-planner.md) — manifesto de evidências
- [agents/plan-decomposer.md](agents/plan-decomposer.md) — fatiamento do plano
- [skills/desafio1-preparacao-implementacao/SKILL.md](skills/desafio1-preparacao-implementacao/SKILL.md) — orquestra Passos 0–4

Todos com **arquivos de escrita exclusivos**, ações proibidas e critério de parada. Nenhum toca em código do desafio.

## 3. Drift registrado (não corrigido)

O kit (`docs/README.md`) referencia `licoesaprendidas/skill/denuncias-quality-review/SKILL.md` e `preparacao-implementacao/agents/*.md`, mas essas pastas estão **vazias** no workspace atual. Os agents deste pacote foram escritos do zero seguindo o padrão descrito no README do kit. Se os originais reaparecerem, reconciliar por diff — não sobrescrever silenciosamente.
