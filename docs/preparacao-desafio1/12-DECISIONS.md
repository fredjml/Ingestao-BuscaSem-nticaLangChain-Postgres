# 12 — Decisões materiais (desafio1)

Data de abertura: 2026-09-04. Regra do kit: conflito material recebe owner e decisão — **nunca** suposição. Estado: todas **ABERTAS**.

| ID | Decisão | Opções | Recomendação | Owner | Estado |
| --- | --- | --- | --- | --- | --- |
| DEC-01 | Estratégia de provider (INC-03/04/07/08/14) | A: só OpenAI. B: só Gemini. C: selecionável por `EMBEDDING_PROVIDER` com coleção separada por provider | — | operador | **FECHADA 2026-09-04 → C** (selecionável via env). Verificar nomes de modelos na fonte oficial com data (INC-07/08) |
| DEC-02 | Origem do código-base (INC-01) | A: fork do template. B: scaffold próprio | — | operador | **FECHADA 2026-09-04 → A** — `github.com/devfullcycle/mba-ia-desafio-ingestao-busca.git` (verificado 2026-09-04, commit init `82d86ce`, branch `main`) |
| DEC-03 | Origem do `document.pdf` (INC-02) | A: usar `document.pdf` do template após verificação. B: sintético de `document-sintetico-fonte.md`. C: ambos | — | operador | **FECHADA 2026-09-04 → C** — **VERIFICADO na A1**: `document.pdf` contém `SuperTechIABrazil R$ 10.000.000,00 2025` (fato de aceite ✔). Sintético fica como fixture de teste offline |
| DEC-04 | Versão mínima do Python (INC-06) | A: 3.12. B: 3.13. C: 3.11 | — | operador | **FECHADA 2026-09-04 → A (3.12)** — compatibilidade com pins do template; confirmar wheels na instalação |
| DEC-05 | Imagem/versão Postgres+pgVector (INC-13) | — | — | — | **FECHADA 2026-09-04 por fonte primária**: template usa `pgvector/pgvector:pg17` + serviço `bootstrap_vector_ext` (`CREATE EXTENSION IF NOT EXISTS vector`). Recomendação anterior (pg16) substituída pelo template |
| DEC-06 | Idempotência da ingestão (INC-09) | A: drop/create da coleção a cada run. B: upsert por hash. C: acumular | — | operador | **FECHADA 2026-09-04 → A** (drop/create — R-INC-01) |
| DEC-07 | Compliance: conteúdo do PDF enviado a API externa (T-03, RNF-PRV-01) | A: autorizado. B: autorizado com restrições. C: bloqueado p/ PDF real | — | operador | **FECHADA 2026-09-04 → A** (autorizado). Controles T-03 mantidos: minimização (só k=10 chunks ao LLM), sem segredos no PDF, evidências sanitizadas |
| DEC-08 | Publicação em repo público GitHub (INC-12) | A: fork público do template. B: repo público novo | — | operador | **FECHADA 2026-09-04 → A** (fork público) — a autorização de push/publicação será pedida just-in-time no Passo 9 |
| DEC-09 | Bind da porta do Postgres no compose (INC-15, T-05) — template publica `5432:5432` em todas as interfaces | A: restringir a `127.0.0.1:5432:5432`. B: manter template | — | operador | **FECHADA 2026-09-04 → A** (`127.0.0.1:5432:5432` — desvio registrado do template) |

**Todas as 9 decisões FECHADAS em 2026-09-04.** Gates 1 e 2 desbloqueados. **Gate 0: GO** (Python 3.12.10 + Docker daemon 29.6.2 ativos em 2026-09-04). **Fatia A1 commitada** (`08bafc4`) e **publicada antecipadamente** (autorização explícita do owner) em `github.com/fredjml/Ingestao-BuscaSem-nticaLangChain-Postgres` (commit de merge `55a50c7`, verificado via `git ls-remote`). Publicação incremental autorizada para as próximas fatias; **entrega formal (Passo 9/Gate 7) segue pendente** até Gates 4/5/6 fecharem.

## Como fechar

Responder por escrito (chat serve) no formato: `DEC-xx: <opção> — <owner> — <data>`. Este arquivo é atualizado e o Gate correspondente é reavaliado. Fechamento de DEC não autoriza implementação por si só (autorização é por ação).
