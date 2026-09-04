# 00 — Mapa de origens, baseline e drift (desafio1)

Data desta atualização: **2026-09-04**. Estado probatório: offline/estático.

## 1. Fontes com precedência

| # | Fonte | Papel | Estado |
| --- | --- | --- | --- |
| 1 | Enunciado do desafio1 (mensagem do operador, 2026-09-04) | **fonte primária** de requisitos | presente (transcrito no chat) |
| 2 | Template `github.com/devfullcycle/mba-ia-desafio-ingestao-busca` (DEC-02 → A) | estrutura obrigatória, compose, skeletons, deps pinadas, `document.pdf` | **PRESENTE** — verificado read-only 2026-09-04 (commit init `82d86ce`, branch `main`) |
| 3 | `document.pdf` (do template) + sintético de `document-sintetico-fonte.md` | insumo de ingestão e da prova de aceite | **DEC-03=C**: template p/ demo (conteúdo a verificar na A1); sintético p/ fixture de teste |
| 4 | `docs/licoesaprendidas/` | controles reutilizáveis (não é fonte de fato) | presente |
| 5 | `docs/Analises/` + `docs/preparacao-implementacao/` (Denúncias) | referência metodológica histórica | presente — **não se aplica como fato ao desafio1** |

Regra do kit: qualquer alegação material exigirá reabertura da fonte primária. "NÃO FOI POSSÍVEL DETERMINAR" é resposta válida.

## 2. Baseline técnica observada (2026-09-04, comandos read-only)

| Item | Observado | Fonte |
| --- | --- | --- |
| Código do desafio | **inexistente** — workspace contém apenas `docs/` | `list_dir` 2026-09-04 |
| Git no workspace | não é repositório (`git rev-parse` → fatal) | terminal 2026-09-04 |
| Python / pip / py launcher | **ausentes** (alias Microsoft Store) | terminal 2026-09-04 |
| Docker client / Compose | 29.6.2 / v5.3.1 | terminal 2026-09-04 |
| Docker daemon | **parado** (pipe dockerDesktopLinuxEngine não encontrado) | terminal 2026-09-04 |
| Node | v24.19.0 (só relevante p/ validador de diagramas do kit) | terminal 2026-09-04 |
| SO/shell | Windows + PowerShell | ambiente da sessão |
| Template — arquivos | `src/{ingest,search,chat}.py` (skeletons com `pass`), `.env.example`, `.gitignore`, `README.md`, `docker-compose.yml`, `document.pdf`, `requirements.txt` | github.com 2026-09-04 |
| Template — compose | `pgvector/pgvector:pg17`, db `rag`, user/pass `postgres/postgres`, porta `5432:5432` (**todas as interfaces** — INC-15), healthcheck + serviço `bootstrap_vector_ext` (`CREATE EXTENSION IF NOT EXISTS vector`) | raw.githubusercontent 2026-09-04 |
| Template — deps | `requirements.txt` 100% pinado: langchain 0.3.27, langchain-openai 0.3.30, langchain-google-genai 2.1.9, langchain-postgres 0.0.15, langchain-text-splitters 0.3.9, pypdf 6.0.0, psycopg[binary] 3.2.9, openai 1.102.0; **sem pytest/pip-audit** (INC-17) | idem |
| Template — `.env.example` | `GOOGLE_API_KEY`, `GOOGLE_EMBEDDING_MODEL='models/embedding-001'`, `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL='text-embedding-3-small'`, `DATABASE_URL`, `PG_VECTOR_COLLECTION_NAME`, `PDF_PATH`; **sem variáveis de LLM** (INC-16) | idem |
| Template — skeletons | `ingest.py` (`PDF_PATH` env + `ingest_pdf(): pass`); `search.py` (`PROMPT_TEMPLATE` idêntico ao enunciado + `search_prompt(): pass`); `chat.py` (importa `search_prompt`, loop esquelético) | github.com 2026-09-04 |

## 3. Inconsistências e lacunas do enunciado (INC-xx)

| ID | Inconsistência / lacuna | Impacto | Tratamento |
| --- | --- | --- | --- |
| INC-01 | ~~Link do fork inacessível~~ **RESOLVIDA 2026-09-04** — URL fornecida pelo owner (DEC-02) e template verificado | — | — |
| INC-02 | ~~`document.pdf` não fornecido~~ **RESOLVIDA 2026-09-04** — DEC-03=C: template tem `document.pdf` (verificação do fato de aceite na A1) + sintético como fixture | — | — |
| INC-03 | ~~Enunciado descreve OpenAI e Gemini sem dizer se é escolha exclusiva~~ **RESOLVIDA 2026-09-04** — DEC-01=C (selecionável via env) | — | — |
| INC-04 | ~~`.env.example` só com `OPENAI_API_KEY`~~ **RESOLVIDA no template** — cobre ambos providers + `DATABASE_URL` + `PDF_PATH`; lacuna residual: sem variáveis de modelo LLM (INC-16) | — | — |
| INC-05 | Comandos Unix-only (`python3`, `source venv/bin/activate`) em ambiente **Windows/PowerShell** | README precisa instruções Windows (`venv\Scripts\Activate.ps1`, execution policy) | requisito RNF-OPS-02 |
| INC-06 | Versão mínima de Python não especificada | LangChain atual exige >=3.9; convém pinar (sugestão 3.11+) | DEC-04 |
| INC-07 | Modelos `gpt-5-nano` e `gemini-3.1-flash-lite-preview` citados sem verificação de disponibilidade/nome na fonte oficial | risco de modelo inexistente/renomeado na data de implementação | verificação obrigatória na Fase B (fonte oficial, com data) |
| INC-08 | `models/embedding-001` (Gemini) é geração antiga (768 dims); pode estar legado/deprecado | escolha de embedding impacta schema do pgvector | verificação obrigatória na Fase B; DEC-01 |
| INC-09 | Idempotência da ingestão não especificada (reexecutar `ingest.py` duplica vetores?) | comportamento de reexecução indefinido | **RESOLVIDA 2026-09-04** — DEC-06=A (drop/create da coleção) |
| INC-10 | Sem threshold de relevância: recusa fora-de-contexto depende **só** do prompt (k=10 sempre retorna algo) | risco de resposta inventada mitigado apenas por prompt | aceito pelo enunciado; mitigação via RF-QRY-04/05 + teste |
| INC-11 | Enunciado **não exige testes**; o kit exige (Gate 4) | suíte mínima com doubles (sem custo de API) entra como requisito | RNF-QA-01/02 |
| INC-12 | Entregável = "repositório público no GitHub", mas depende de fork (INC-01) e de autorização de publicação | Gate 7 bloqueado até owner autorizar | DEC-08 |
| INC-13 | ~~Versão do Postgres/pgvector e criação da extensão~~ **RESOLVIDA no template** — `pgvector/pgvector:pg17` + `bootstrap_vector_ext` | — | DEC-05 fechada por fonte primária |
| INC-14 | Limites free-tier (Gemini/OpenAI) mudam com frequência — o próprio enunciado admite | risco operacional de cota | registrado em riscos; DEC-01 fechada |
| INC-15 | Compose do template publica `5432:5432` em **todas as interfaces** | exposição do Postgres na rede local (T-05) | **RESOLVIDA 2026-09-04** — DEC-09=A (`127.0.0.1:5432`, desvio registrado) |
| INC-16 | Template não define variáveis de modelo LLM (`OPENAI_LLM_MODEL`/`GEMINI_LLM_MODEL`) | contrato de env incompleto p/ `chat.py` | adição planejada em 08-TDD §2 (desvio registrado do template) |
| INC-17 | `requirements.txt` do template não inclui `pytest`/`pip-audit` | kit exige testes com doubles (Gate 4) | adição como **desvio registrado** do template |

## 4. Limitações desta atualização

- Nenhum comando além de verificações de versão foi executado localmente; a verificação do template foi read-only via web (2026-09-04), sem clone.
- Conteúdo de `document.pdf` do template **não verificado** (binário) — verificar na fatia A1 se contém o fato de aceite ("faturamento SuperTechIABrazil = 10 milhões de reais").
- Existência/nomenclatura de modelos OpenAI/Gemini **não verificada** na fonte oficial — fazer na Fase B com data.
- Compatibilidade dos pins do template com a versão de Python a instalar (DEC-04) será confirmada na instalação.
