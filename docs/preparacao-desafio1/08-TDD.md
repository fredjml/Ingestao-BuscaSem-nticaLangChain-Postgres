# 08 — TDD / desenho técnico (desafio1)

Data: 2026-09-04. Baseado no enunciado; nada implementado. Contratos marcados **(DEC)** dependem de decisão aberta.

## 1. Componentes

| Componente | Responsabilidade | Depende de |
| --- | --- | --- |
| `src/ingest.py` | load PDF → split 1000/150 → embed → PGVector.from_documents | `.env`, PDF, banco up |
| `src/search.py` | `buscar(pergunta) -> list[(Document, score)]` via `similarity_search_with_score(k=10)` | mesma config de embeddings da ingestão |
| `src/chat.py` | loop CLI → `search.buscar` → monta prompt fixo → LLM → imprime | `search.py`, LLM provider |
| `docker-compose.yml` (do template) | `pgvector/pgvector:pg17`, db `rag`, user/pass dev `postgres/postgres`, healthcheck + `bootstrap_vector_ext`; bind `127.0.0.1:5432:5432` (DEC-09) | DEC-05 fechada: pg17 |
| `tests/` | pytest com doubles (embeddings/LLM/DB falsos) | nenhuma credencial |

## 2. Contrato de configuração (`.env` / `.env.example`)

```
# base do template (.env.example verificado 2026-09-04)
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
GOOGLE_API_KEY=
GOOGLE_EMBEDDING_MODEL=models/embedding-001      # verificar deprecação (INC-08)
DATABASE_URL=postgresql+psycopg://postgres:***@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=desafio1               # sufixo por provider (dims 1536 vs 768)
PDF_PATH=./document.pdf
# adições nossas (INC-16) — verificar nomes na fonte oficial com data (INC-07)
EMBEDDING_PROVIDER=openai|gemini                 # DEC-01=C
OPENAI_LLM_MODEL=gpt-5-nano
GEMINI_LLM_MODEL=gemini-2.5-flash-lite
```

Regra: **nunca** valores reais no `.env.example`; connection string montada a partir das variáveis (sem segredo em código).

## 3. Contrato de dados

- Coleção PGVector por provider (`PG_VECTOR_COLLECTION_NAME` + sufixo do provider) — misturar dims no mesmo store quebra o schema (1536 OpenAI vs 768 Gemini).
- Idempotência (**DEC-06=A**): `ingest.py` faz **drop/create da coleção** a cada execução — reexecução nunca duplica vetores (RF-ING-05).
- Metadados mínimos por chunk: `source=document.pdf`, `page` (do loader).

## 4. Sequência ponta-a-ponta

```mermaid
sequenceDiagram
  participant U as Usuário
  participant C as chat.py
  participant S as search.py
  participant E as API Embeddings
  participant P as PGVector (Docker)
  participant L as API LLM
  U->>C: pergunta
  C->>S: buscar(pergunta)
  S->>E: embed(pergunta)
  S->>P: similarity_search_with_score(k=10)
  P-->>S: 10 chunks + scores
  S-->>C: chunks
  C->>L: prompt fixo + contexto + pergunta
  L-->>C: resposta (ou frase exata de recusa)
  C-->>U: RESPOSTA
```

## 5. Estratégia de testes (Gate 4)

| Nível | Prova | Não prova |
| --- | --- | --- |
| unit (pytest, doubles) | splitter 1000/150; template do prompt byte-a-byte; fallback; k=10; parsing de `.env` | API real, banco real |
| integ-sim | chat orquestra search→prompt→LLM com fakes | contrato real da API |
| live local autorizado | ingest real + 1 pergunta in-context + 1 out-of-context | produção, carga, disponibilidade |

Comandos candidatos (Fase B, após instalação): `pytest -q`, `docker compose up -d`, `python src/ingest.py`, `python src/chat.py`. Registrar commit+data+exit code em `07-TRACEABILITY.md`.

## 6. Limitações

- Nomes de modelos (INC-07/08) e assinaturas exatas das libs serão verificados na fonte oficial **na data da implementação** — este desenho não os trata como fato.
