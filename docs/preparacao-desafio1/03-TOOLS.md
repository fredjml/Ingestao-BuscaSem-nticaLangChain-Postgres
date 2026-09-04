# 03 — Inventário de ferramentas (desafio1)

Data: 2026-09-04. Critério do kit: escolher ferramenta por **requisito, risco, licença, telemetria e fallback**. Nada é instalado por este documento.

## 1. Obrigatórias (do enunciado)

| Ferramenta | Requisito que atende | Risco/observação | Fallback |
| --- | --- | --- | --- |
| Python 3.11+ (venv + pip) | todo o runtime | ausente no host (pre-flight) | — |
| Docker Desktop + Compose v2 | RNF-OPS-01 (Postgres+pgVector) | daemon parado; bind em 127.0.0.1 | — |
| Git | versionamento + entrega GitHub | workspace não é repo (DEC-02) | scaffold com `git init` |
| `langchain`, `langchain-text-splitters` | RF-ING-02 | versões pinadas em requirements.txt | — |
| `langchain-openai` | RF-ING-03/RF-QRY-02 (OpenAI) | custo/cota; chave em `.env` | provider Gemini (DEC-01) |
| `langchain-google-genai` | RF-ING-03/RF-QRY-02 (Gemini) | cota free-tier instável (INC-14) | provider OpenAI (DEC-01) |
| `langchain-community` (PyPDFLoader) | RF-ING-01 | parse local, sem execução de conteúdo | `pypdf` direto |
| `langchain-postgres` (PGVector) | RF-ING-04/RF-QRY-03 | cria extensão/tabelas; dims por provider | — |
| `psycopg[binary]` (driver PG) | RF-ING-04 | preferir binary p/ Windows | — |
| `python-dotenv` | RNF-SEC-01 | nunca logar valores | `os.environ` |

## 2. Recomendadas pelo kit (não pelo enunciado)

| Ferramenta | Requisito | Justificativa |
| --- | --- | --- |
| `pytest` | RNF-QA-01/02 | testes com doubles — zero custo de API |
| `pip-audit` (ou equivalente) | T-04 supply chain | scan de advisories; registrar com data |

## 3. Vetadas sem autorização adicional

- Qualquer ferramenta que envie código ou PDF a terceiros além das APIs do enunciado.
- CLIs de cloud (gcloud/az/aws) — fora de escopo.
- Instalação global de pacotes Python (skill `managing-python-dependencies`: sempre venv).

## 4. Telemetria

Ferramentas listadas não exigem telemetria habilitada. Se alguma solicitar, registrar aqui com data e decisão do owner.
