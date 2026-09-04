# 06 — Requisitos (desafio1)

Data: 2026-09-04. Fonte/local citado por requisito. Confiança: **A**lta (explícito no enunciado), **M**édia (inferência do enunciado), **B**aixa (proposta do kit — exige aceite). Escopo negativo em [05-PRD.md](05-PRD.md).

## Requisitos funcionais

| ID | Prio | Requisito | Aceite (Dado/Quando/Então) | Fonte | Conf. |
| --- | --- | --- | --- | --- | --- |
| RF-ING-01 | P0 | Carregar `./document.pdf` com `PyPDFLoader` | Dado um PDF válido em `./document.pdf`, Quando `ingest.py` executa, Então o documento é carregado sem erro | enunciado §Requisitos 1 | A |
| RF-ING-02 | P0 | Split com `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)` | Dado o PDF carregado, Quando o split ocorre, Então os parâmetros são exatamente 1000/150 | enunciado §Requisitos 1 | A |
| RF-ING-03 | P0 | Gerar embedding por chunk com o provider configurado (DEC-01) | Dado os chunks, Quando a ingestão roda, Então cada chunk tem embedding do provider vigente | enunciado §Tecnologias | A |
| RF-ING-04 | P0 | Persistir vetores via `langchain_postgres.PGVector` no Postgres+pgVector do compose | Dado os embeddings, Quando a ingestão conclui, Então os vetores estão no banco e contam-se N chunks | enunciado §Requisitos 1 | A |
| RF-ING-05 | P1 | Reexecução da ingestão não duplica registros — **drop/create da coleção** a cada run (DEC-06) | Dado um banco já populado, Quando `ingest.py` roda de novo, Então a coleção é recriada e a contagem final = N chunks do PDF | INC-09 + DEC-06 (2026-09-04) | A |
| RF-QRY-01 | P0 | CLI interativo com loop "Faça sua pergunta:" e comando de saída | Dado o chat iniciado, Quando o usuário pergunta, Então recebe resposta; Quando digita saída (`sair`/`exit`), Então encerra | enunciado §Consulta via CLI | A |
| RF-QRY-02 | P0 | Vetorizar a pergunta com o **mesmo** provider de embeddings da ingestão | Dada uma pergunta, Quando a busca inicia, Então o embedding usa o provider configurado | enunciado §Consulta passo 1 | A |
| RF-QRY-03 | P0 | `similarity_search_with_score(pergunta, k=10)` | Dada a pergunta vetorizada, Quando busca, Então retorna até 10 chunks com score | enunciado §Busca | A |
| RF-QRY-04 | P0 | Manter o **prompt exato** (CONTEXTO + REGRAS + 3 exemplos + PERGUNTA DO USUÁRIO) — já presente como `PROMPT_TEMPLATE` em `src/search.py` do template | Dados os 10 chunks, Quando monta o prompt, Então o texto é byte-a-byte o do template/enunciado (contexto/pergunta interpolados) | enunciado §Prompt + template `src/search.py` (verificado 2026-09-04) | A |
| RF-QRY-05 | P0 | Fora de contexto → responder **exatamente** `Não tenho informações necessárias para responder sua pergunta.` | Dada pergunta sem resposta no contexto (ex.: "Quantos clientes temos em 2024?"), Quando a LLM responde, Então a saída é a frase exata de recusa | enunciado §Exemplo | A |
| RF-QRY-06 | P1 | `search.py` expõe função de busca reutilizável por `chat.py` (sem lógica duplicada) | Dado o módulo search, Quando chat.py importa, Então usa a função pública de busca | enunciado §Estrutura | M |

## Requisitos não funcionais

| ID | Prio | Requisito | Aceite | Fonte | Conf. |
| --- | --- | --- | --- | --- | --- |
| RNF-SEC-01 | P0 | Segredos só em `.env` (gitignored); `.env.example` cobre provider(s) + Postgres **sem valores** | Dado o repo, Quando se busca padrão de chave, Então nenhum segredo versionado; `.env.example` lista todas as variáveis exigidas | enunciado §Estrutura + INC-04 | A |
| RNF-SEC-02 | P0 | Nenhum segredo/PII em logs, prompts de IA ou artifacts (R-SEC-01) | Dado qualquer log/evidência, Quando inspecionado, Então sem chaves/PII | kit | A |
| RNF-PRV-01 | P0 | Conteúdo do PDF é enviado a API externa (embeddings+LLM) — **DEC-07** antes de PDF real | Dado um PDF com dado não público, Quando faltar DEC-07, Então ingestão live fica BLOQUEADA | T-03 | A |
| RNF-OPS-01 | P0 | `docker compose up -d` sobe Postgres+pgVector com extensão criada — template: `pgvector/pgvector:pg17`, db `rag`, serviço `bootstrap_vector_ext` | Dado o compose, Quando sobe, Então extensão `vector` presente e bind de porta conforme DEC-09 | enunciado §Ordem + template `docker-compose.yml` (2026-09-04) + T-05 | A |
| RNF-OPS-02 | P0 | README com ordem compose→ingest→chat, **com instruções Windows e Unix** (INC-05) | Dado um operador Windows, Quando segue o README, Então ativa venv e executa sem erro | enunciado + INC-05 | A |
| RNF-OPS-03 | P1 | `requirements.txt` pinado (já no template) + **adição** de `pytest`/`pip-audit` como desvio registrado (INC-17); venv documentado | Dado o repo, Quando `pip install -r requirements.txt`, Então resolve versões exatas | kit (supply chain) + template (2026-09-04) | A |
| RNF-QA-01 | P1 | Testes unitários com **doubles** (embeddings/LLM/DB) — zero chamada real (INC-11) | Dado `pytest`, Quando executa offline, Então tudo passa sem rede | kit Gate 4 | B |
| RNF-QA-02 | P1 | Testes cobrem: parâmetros do splitter (1000/150), template do prompt e regra de fallback | Dado o suíte, Quando roda, Então RF-ING-02, RF-QRY-04 e RF-QRY-05 têm caso de teste | kit Gate 4 | B |

## Exclusões / escopo negativo

Ver [05-PRD.md §Escopo negativo](05-PRD.md). Nenhuma exclusão do enunciado foi assumida sem registro — itens não exigidos pelo enunciado mas exigidos pelo kit (RNF-QA-*) estão marcados conf. **B** e aguardam aceite do owner.

## Lacunas abertas

**Nenhuma** — as 9 DECs foram fechadas em 2026-09-04. **Gate 1: FECHADO.** Pendências remanescentes são de ambiente (Gate 0): instalar Python 3.12, iniciar Docker daemon, credenciais do owner.
