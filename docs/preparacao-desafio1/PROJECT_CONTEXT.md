# PROJECT_CONTEXT — desafio1 (Ingestão e Busca Semântica LangChain + Postgres)

> Regra do kit: manter em até duas páginas. Não reler, salvo mudança.

- **Objetivo/fonte**: desafio1 — software CLI em Python que (1) ingere um PDF em PostgreSQL+pgVector via LangChain e (2) responde perguntas **somente** com base no conteúdo do PDF. Fontes primárias: **enunciado** (2026-09-04) + **template** `devfullcycle/mba-ia-desafio-ingestao-busca` (DEC-02=A, verificado 2026-09-04, commit `82d86ce`). Provider selecionável via env (DEC-01=C). Envio do PDF a APIs externas autorizado (DEC-07=A).
- **Commit/ambiente**: workspace `Ingestao&BuscaSemânticaLangChain&Postgres` — **greenfield**, sem código, **não é repo git** (verificado 2026-09-04). Host: Windows + PowerShell. Python **ausente**; Docker client 29.6.2 / Compose v5.3.1 presentes, **daemon parado**; git 2.55.0; node v24.19.0.
- **Requisito/fatia ativa**: pré-implementação — Passos 0 a 4 do [kit](../licoesaprendidas/README.md). Nenhuma fatia de código autorizada.
- **Estado probatório**: **offline/estático**. Comandos executados: apenas verificações de versão read-only (registradas em [02-PRE-FLIGHT.md](02-PRE-FLIGHT.md)). Nenhum número de relatório antigo é usado como fato.
- **Decisão vigente e motivo**: pacote de preparação gerado antes de qualquer código. **Todas as 9 DECs FECHADAS** (2026-09-04): provider selecionável via env; fork do template; PDF do template (demo) + sintético (fixture); Python 3.12; pgvector pg17; drop/create por ingestão; envio a API externa autorizado; fork público na entrega; bind 127.0.0.1. Gates 1/2 fechados; Gate 0 de implementação pendente de ambiente.
- **Arquivos alterados**: somente dentro de `docs/preparacao-desafio1/`. Nada fora desta pasta foi criado/modificado.
- **Último comando/resultado**: fatia A1 **commitada** (`08bafc4`) — clone do template + desvios autorizados aplicados. Python 3.12.10 + pip 26.1.2 instalados; Docker daemon 29.6.2 ativo; pre-flight **GO**.
- **Evidência**: leitura do enunciado + saída de terminal do pre-flight. Sanitizada por natureza (sem PII, secrets ou logs de serviço).
- **Bloqueio/owner**:
  - Owner do desafio (produto): **operador humano** — DEC-01/02/05/07 assinadas em 2026-09-04.
  - DEC-07 (envio do PDF a API externa): **autorizado** pelo owner em 2026-09-04.
  - Owner de credenciais (OpenAI/Google API keys): **pendente** — nunca colar valores no chat.
  - Owner de infra (instalar Python, iniciar Docker daemon): **pendente**.
- **Autorização vigente e limites**: **somente leitura/documentação nesta pasta**. Vetado: instalação, código, execução de serviços, live, commit/push, dado real.
- **Próximo passo único**: Fase B — fatia **A2** (implementar `ingest.py`: load PDF → split 1000/150 → embed → PGVector, com drop/create da coleção). Autorização just-in-time por fatia via [13-PROMPTS.md](13-PROMPTS.md) §Passo 5.
- **Links para detalhes**: [ANALYSIS](01-ANALYSIS.md), [PRD](05-PRD.md), [REQUIREMENTS](06-REQUIREMENTS.md), [TDD](08-TDD.md), [THREAT MODEL](09-THREAT-MODEL.md), [PLAN](11-IMPLEMENTATION-PLAN.md), [PROMPTS](13-PROMPTS.md).
- **Não reler, salvo mudança**: fontes citadas em [00-MAPA-ORIGENS.md](00-MAPA-ORIGENS.md).
