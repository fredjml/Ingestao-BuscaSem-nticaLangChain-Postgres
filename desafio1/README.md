# Desafio MBA Engenharia de Software com IA - Full Cycle

Ingestão e busca semântica sobre um PDF usando LangChain + PostgreSQL/pgVector, com respostas via LLM (OpenAI ou Google Gemini) restritas ao conteúdo do documento.

## Pré-requisitos

- Python 3.12
- Docker Desktop (com o daemon em execução)
- Uma chave de API válida da [OpenAI](https://platform.openai.com/api-keys) e/ou do [Google AI Studio](https://aistudio.google.com/apikey)

## 1. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha suas chaves:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` e preencha pelo menos os campos do provider escolhido:

```dotenv
GOOGLE_API_KEY=            # obrigatório se EMBEDDING_PROVIDER=gemini
OPENAI_API_KEY=            # obrigatório se EMBEDDING_PROVIDER=openai
EMBEDDING_PROVIDER=openai  # "openai" ou "gemini"
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/rag
PG_VECTOR_COLLECTION_NAME=desafio1
PDF_PATH=./document.pdf
```

> O `.env` nunca é commitado (está no `.gitignore`). Não compartilhe suas chaves.

## 2. Subir o banco de dados (PostgreSQL + pgVector)

```powershell
docker compose up -d
```

Isso sobe o container `postgres_rag` e cria a extensão `vector` automaticamente. Aguarde o status `healthy`:

```powershell
docker compose ps
```

## 3. Criar o ambiente virtual e instalar as dependências

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Ingerir o PDF

Coloca o PDF no caminho apontado por `PDF_PATH` (por padrão `./document.pdf`, já incluso neste repositório) e execute:

```powershell
python src\ingest.py
```

Isso divide o PDF em chunks, gera os embeddings (via `EMBEDDING_PROVIDER`) e indexa tudo na coleção `PG_VECTOR_COLLECTION_NAME` do Postgres.

## 5. Fazer perguntas via CLI

```powershell
python src\chat.py
```

Exemplo de uso:

```
Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento da SuperTechIABrazil é de R$ 10.000.000,00.

Faça sua pergunta: Qual é a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Digite `sair`, `exit` ou `quit` para encerrar.

## 6. Rodar os testes

```powershell
pytest
```

## Trocar de provider (OpenAI ↔ Gemini)

Altere `EMBEDDING_PROVIDER` no `.env` para `openai` ou `gemini` e rode novamente `src\ingest.py` — cada provider usa sua própria coleção (`{PG_VECTOR_COLLECTION_NAME}_{provider}`), evitando misturar embeddings de dimensões diferentes.

## Encerrar o ambiente

```powershell
docker compose down
```

Use `docker compose down -v` para também apagar o volume de dados do Postgres.