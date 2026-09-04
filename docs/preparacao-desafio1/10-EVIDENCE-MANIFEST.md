# 10 — Evidence Manifest (desafio1)

Data: 2026-09-04. Regra do kit: content freeze → captura → sanitização → inspeção → ligação commit/versão → retenção. Evidência aumenta confiança; não prova veracidade absoluta.

## 1. Shot list

| ID | Tela/estado | Requisito | Ambiente/modo | Mostrar | Ocultar | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| EV-01 | terminal: `docker compose up -d` + `docker ps` + verificação da extensão `vector` | RNF-OPS-01 | live local | container up, porta 127.0.0.1 | senhas, strings de conexão | ausente |
| EV-02 | execução `python src/ingest.py` — "N chunks indexados" | RF-ING-01..05 | live local | contagem final de chunks | valores de env, caminhos de usuário | ausente |
| EV-03 | chat: pergunta **in-context** (faturamento SuperTechIABrazil) → resposta fundamentada | RF-QRY-01/03/04 | live local | pergunta + resposta | qualquer dado fora do esperado | ausente |
| EV-04 | chat: pergunta **fora de contexto** → frase exata de recusa | RF-QRY-05 | live local | pergunta + resposta exata | idem | ausente |
| EV-05 | `pytest -q` verde (offline, doubles) | RNF-QA-01/02, RF-ING-02, RF-QRY-03/04 | unit | resumo de testes, exit code | paths de usuário | ausente |
| EV-06 | `git status` + grep de segredos antes de qualquer commit | RNF-SEC-01/02 | estático | ausência de `.env` nos stage/tracked | — | ausente |

## 2. Regras de sanitização

- Nunca capturar: API keys, `POSTGRES_PASSWORD`, connection string completa, paths `C:\Users\...`, conteúdo sensível do PDF além do necessário à prova.
- Fixture de testes automatizados = **PDF sintético** gerado de `document-sintetico-fonte.md` (DEC-03=C); PDF do template só em live local autorizado.
- Toda evidência registra: data/hora, commit, comando exato, exit code, limitação.

## 3. Content freeze

Antes de EV-03/EV-04: congelar prompt, PDF e código da fatia; regerar se a fonte mudar.

## 4. Retenção e acesso

Local de arquivamento: `docs/preparacao-desafio1/evidencias/` (a criar na Fase B, com autorização). Acesso: owner do ciclo. Retenção: até aceite + RCA (Passo 10).

## 5. Limitações

Screenshot/log pode omitir erro ou ser manipulado; teste live pontual não prova disponibilidade. "Não foi possível determinar" é registro válido.
