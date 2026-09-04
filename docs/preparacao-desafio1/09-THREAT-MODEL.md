# 09 — Threat Model (desafio1)

Data: 2026-09-04. Escopo: app CLI local + Postgres em Docker + APIs externas de embeddings/LLM. Veto do kit: sem DAST/pentest; checklist não substitui DPO/jurídico.

## 1. Ativos

- **A1** Conteúdo do `document.pdf` (pode conter dado de negócio — ex.: faturamento; possivelmente PII).
- **A2** API keys OpenAI/Google.
- **A3** Credenciais do Postgres local.
- **A4** Chunks+embeddings persistidos (derivados de A1 — equivalente semântico do conteúdo).
- **A5** Integridade das respostas (sem alucinação fora do contexto).

## 2. Trust boundaries

| TB | Fronteira | Notas |
| --- | --- | --- |
| TB-1 | host ↔ container Postgres (Docker) | local; bind 127.0.0.1 |
| TB-2 | app ↔ OpenAI API (internet/TLS) | **conteúdo do PDF sai da máquina** (embeddings na ingestão; top-10 chunks por pergunta) |
| TB-3 | app ↔ Google API (internet/TLS) | idem |
| TB-4 | repo local ↔ GitHub público (entrega) | risco de vazar `.env`/PDF |

## 3. Ameaças e controles

| ID | Ameaça | Ativo | Controle | Residual |
| --- | --- | --- | --- | --- |
| T-01 | Commit acidental de `.env`/segredo | A2/A3 | `.gitignore` + `.env.example` sem valores + grep de segredos no review (Passo 8) + gate antes de push | baixo |
| T-02 | Prompt injection embutida no PDF ("ignore as regras…") | A5 | prompt fixo rígido; LLM **sem tools**; saída só texto; saída nunca executada como código; teste de fallback | médio (inerente a RAG) |
| T-03 | Exfiltração de dado do PDF p/ API externa | A1/A4 | **DEC-07 AUTORIZADA 2026-09-04**; controles mantidos: só k=10 chunks ao LLM, sem segredos no PDF, evidências sanitizadas | baixo |
| T-04 | Supply chain (deps pip maliciosas/vulneráveis) | app | requirements pinados + `pip-audit` com data; sem deps fora de [03-TOOLS.md](03-TOOLS.md) | baixo |
| T-05 | Postgres exposto na rede — template publica `5432:5432` em todas as interfaces (INC-15) | A3/A4 | **DEC-09=A (2026-09-04)**: bind `127.0.0.1:5432:5432`; senha dev-only no `.env` | baixo |
| T-06 | Alucinação fora de contexto (sem threshold — INC-10) | A5 | prompt fixo + 3 few-shots de recusa + frase exata + teste RF-QRY-05 | médio |
| T-07 | Abuso de cota/custo de API | A2 | chaves com quota no console do owner; k=10 limita tokens; modelos nano/flash-lite; testes com doubles | baixo |
| T-08 | PDF malformado/malicioso quebra o loader | app | parse local sem execução; erro tratado com mensagem limpa; sem PDF de fonte desconhecida (DEC-03) | baixo |
| T-09 | Segredo em log/traceback | A2/A3 | nunca logar env; tracebacks sem valores; evidências sanitizadas (R-SEC-01) | baixo |

## 4. Estados probatórios relevantes

- ClamAV-like scanning: **não aplicável** (PDF local de fonte controlada — DEC-03).
- "FEITO LIVE" só vale para o ambiente local autorizado; nada aqui prova produção.
- Fail-closed: se a API externa falhar, o chat deve falhar com mensagem limpa — **nunca** responder de cache/conhecimento externo (coerente com RF-QRY-05).

## 5. Decisões de segurança pendentes

**Nenhuma.** DEC-07 (envio autorizado) e DEC-09 (bind 127.0.0.1) fechadas em 2026-09-04. **Gate 2: FECHADO.** Controles de T-02/T-06 seguem como risco residual aceito (mitigados por prompt fixo + testes).

## 6. Limitações

Sem DAST/pentest; sem análise do PDF real (ausente — INC-02); disponibilidade dos modelos não verificada (INC-07/08).
