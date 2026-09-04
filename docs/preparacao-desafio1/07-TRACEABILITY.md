# 07 — Rastreabilidade (desafio1)

Data: 2026-09-04. Estados: **NE**=não executado, INC=inconclusivo, FAIL, OK. Modos: estático, unit, integ-sim, live, UI-manual. Regra do kit: modo não é intercambiável; resultado histórico não prova estado atual.

| ID | Fonte | Artefato | Implementação (prevista) | Teste/modo | Resultado | Evidência | Entrega | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RF-ING-01 | enunciado §Req1 | `src/ingest.py` | fatia A2 (`374390e`) | unit (double loader, via orquestração) | OK | pytest 8/8 verde | local | fred |
| RF-ING-02 | enunciado §Req1 | `src/ingest.py` | fatia A2 (`374390e`) | unit (assert 1000/150) | OK | `test_split_documents_uses_1000_150` | local | fred |
| RF-ING-03 | enunciado §Tec | `src/ingest.py` | fatia A2 (`374390e`) | unit (double embeddings, sem rede) | OK | `test_get_embeddings_openai_default` + `_gemini` | local | fred |
| RF-ING-04 | enunciado §Req1 | `src/ingest.py` | fatia A2 (`374390e`) | unit (mock PGVector.from_documents) | OK | `test_build_vector_store_uses_pre_delete_collection` | local | fred |
| RF-ING-05 | INC-09 | `src/ingest.py` | fatia A2 (`374390e`) | unit (assert pre_delete_collection=True) | OK | idem acima (DEC-06 verificado) | local | fred |
| RF-QRY-01 | enunciado §CLI | `src/chat.py` | — | live local | NE | EV-03/EV-04 | local | pendente |
| RF-QRY-02 | enunciado §CLI | `src/search.py` | — | unit (double) | NE | EV-05 | local | pendente |
| RF-QRY-03 | enunciado §Busca | `src/search.py` | — | unit (double k=10) + live | NE | EV-05/EV-03 | local | pendente |
| RF-QRY-04 | enunciado §Prompt | `src/chat.py` | — | unit (template exato) | NE | EV-05 | local | pendente |
| RF-QRY-05 | enunciado §Exemplo | `src/chat.py` | — | unit (fallback) + live | NE | EV-04 | local | pendente |
| RF-QRY-06 | enunciado §Estrutura | `src/search.py` | — | estático (import) | NE | EV-05 | local | pendente |
| RNF-SEC-01 | enunciado+INC-04 | `.env.example`, `.gitignore` | — | estático (grep de segredos) | NE | EV-06 | local | pendente |
| RNF-SEC-02 | kit R-SEC-01 | todos | — | review (Passo 8) | NE | — | local | pendente |
| RNF-PRV-01 | T-03 | — (decisão) | — | DEC-07 assinada | NE | — | — | DPO/owner |
| RNF-OPS-01 | enunciado §Ordem | `docker-compose.yml` | — | live local (`docker ps` + extensão) | NE | EV-01 | local | pendente |
| RNF-OPS-02 | enunciado+INC-05 | `README.md` | — | estático + execução guiada | NE | EV-03 | publicada (DEC-08) | pendente |
| RNF-OPS-03 | kit | `requirements.txt` | — | estático (pins) + `pip install` | NE | EV-05 | local | pendente |
| RNF-QA-01 | kit Gate 4 | `tests/` | — | unit offline | NE | EV-05 | local | pendente |
| RNF-QA-02 | kit Gate 4 | `tests/` | — | unit offline | NE | EV-05 | local | pendente |

**Bloqueios de modo**: todo teste `live` exige DEC-01/03/07 fechadas + credenciais do owner + daemon Docker ativo.
