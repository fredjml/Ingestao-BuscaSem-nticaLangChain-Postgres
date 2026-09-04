# 05 — PRD executivo (desafio1)

Data: 2026-09-04. Fonte primária: enunciado do desafio.

## Problema

Precisa-se de um software de linha de comando que responda perguntas **exclusivamente** com base no conteúdo de um PDF, usando busca semântica (RAG) — sem inventar fatos nem usar conhecimento externo.

## Objetivo mensurável

1. **Ingestão**: `python src/ingest.py` carrega `./document.pdf`, divide em chunks de 1000 chars (overlap 150), gera embeddings e grava em Postgres+pgVector.
2. **Busca**: `python src/chat.py` responde perguntas com base nos 10 chunks mais relevantes.
   - Pergunta dentro do contexto (ex.: faturamento da Empresa SuperTechIABrazil) → resposta fundamentada.
   - Pergunta fora do contexto → **exatamente**: `Não tenho informações necessárias para responder sua pergunta.`

## Escopo positivo

- 3 scripts (`ingest.py`, `search.py`, `chat.py`) + `docker-compose.yml` + `requirements.txt` + `.env.example` + `README.md`.
- Postgres+pgVector via Docker Compose; embeddings e LLM via API externa (OpenAI e/ou Gemini — DEC-01).
- Prompt fixo do enunciado, sem alterações de redação.
- Suíte de testes com doubles (exigência do kit, não do enunciado — INC-11).

## Escopo negativo (não fazer)

- Interface web/UI gráfica; API HTTP; streaming.
- Ingestão de múltiplos PDFs ou formatos além de PDF.
- Autenticação de usuários; multiusuário.
- Deploy em nuvem; CI/CD.
- Threshold numérico de relevância (enunciado não pede — INC-10).
- Qualquer refactor além da estrutura obrigatória (R-SCOPE-01).

## Personas e fluxo

- **Operador/avaliador**: sobe o banco (`docker compose up -d`), ingere (`ingest.py`), conversa (`chat.py`). Ordem de execução é requisito do enunciado e do README (RNF-OPS-02).

## Critérios de sucesso (ligam-se ao DoD do kit)

- Aceite do enunciado demonstrado em live local autorizado: 1 pergunta in-context respondida + 1 out-of-context com a frase exata de recusa (evidências EV-03/EV-04 de [10-EVIDENCE-MANIFEST.md](10-EVIDENCE-MANIFEST.md)).
- Testes locais com doubles verdes (RNF-QA-01/02).
- Repo público publicado **somente** após DEC-08 (autorização) e Gate 7.

## Riscos de produto

- Dependência de cota/custo de API externa (INC-14); modelo citado pode não existir na data (INC-07) — fallback registrado em DEC-01.
- Conteúdo do PDF sai da máquina (DEC-07 — compliance).

## Fora deste PRD

Decisões de provider, origem do PDF e publicação: [12-DECISIONS.md](12-DECISIONS.md).
