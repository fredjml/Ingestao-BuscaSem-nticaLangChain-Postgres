# 11 — Plano de implementação incremental (desafio1)

Data: 2026-09-04. **Nenhuma fatia autorizada.** Cada fatia exige: DoR da fatia + owner + autorização just-in-time registrada em [12-DECISIONS.md](12-DECISIONS.md). Regras vinculadas: R-INC-01, R-SCOPE-01, R-QA-01 (teste vermelho antes), R-SEC-01, R-LOOP-01.

## Pré-condições de TODAS as fatias (Gate 0/1/2)

- [x] **Todas as 9 DECs fechadas** em 2026-09-04 (ver 12-DECISIONS.md) → Gates 1 e 2 FECHADOS
- [ ] Python 3.12 instalado (DEC-04); Docker daemon ativo; pre-flight reexecutado (GO) → Gate 0
- [ ] Credenciais do(s) provider(s) configuradas pelo owner (nunca no chat)

## Fatias

| Fatia | Escopo (arquivos permitidos) | Teste focal (vermelho→verde) | Gates | Depende de |
| --- | --- | --- | --- | --- |
| **A1** Clone + ajustes de scaffold + PDF | clone do template (DEC-02); desvios autorizados: adicionar `pytest`/`pip-audit` (INC-17), variáveis LLM no `.env.example` (INC-16), bind `127.0.0.1:5432` (DEC-09); **verificar se `document.pdf` do template contém o fato de aceite**; gerar PDF sintético de `document-sintetico-fonte.md` como fixture de teste (DEC-03=C) | estático: `docker compose config` válido; grep de segredos = 0; PDF do template abre e contém "SuperTechIABrazil"; fixture sintético gerado | 3→4 | Gate 0 (Python + daemon) |
| **A2** Ingestão | `src/ingest.py`, `tests/test_ingest.py`, `pytest.ini` | unit: splitter 1000/150 e pipeline com doubles | 3→4 **FECHADO** (`374390e`, 8/8 verde) | A1, DEC-01/06 |
| **B1** Busca | `src/search.py`, `tests/test_search.py` | unit: `similarity_search_with_score(k=10)` com store fake | 3→4 **FECHADO** (`72df660`, 8/8 verde) | A2 |
| **B2** Chat/CLI | `src/chat.py`, `tests/test_chat.py` | unit: prompt byte-a-byte + fallback exato (LLM fake) | 3→4 **FECHADO** (`4dabd76`, 7/7 verde) | B1 |
| **C1** Live local | (sem código novo; só execução) | EV-01..EV-04 capturadas e sanitizadas | 4 (live) | B2 + credenciais + daemon + PDF verificado (DEC-03) |
| **C2** Fechamento | `README.md` final, evidências | EV-05/EV-06; review Passo 8 | 5→6 | C1 |

Rollback por fatia: cada fatia é auto-contida; reverter = descartar os arquivos da fatia (git). Sem migração de dados.

## Dependências, owners e autorizações

- Owner de todas as fatias: **operador humano (a nomear por fatia em 12-DECISIONS.md)**.
- C1 exige autorização **adicional** de live + credenciais (kit: plano aprovado não autoriza live).
- Publicação GitHub (Passo 9) exige DEC-08 — fora destas fatias.

## Ordem

A1 → A2 → B1 → B2 → C1 → C2. Se uma fatia falhar 2× sem nova hipótese (R-LOOP-01): parar e escalar com o formato de `licoesaprendidas/10-escalonamento.md`.
