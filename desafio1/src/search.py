import os

from dotenv import load_dotenv
from langchain_postgres import PGVector

from ingest import collection_name_for, get_embeddings

load_dotenv()

TOP_K = 10

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_vector_store(embeddings=None, collection_name=None, connection=None):
    return PGVector(
        embeddings=embeddings or get_embeddings(),
        collection_name=collection_name or collection_name_for(),
        connection=connection or os.getenv("DATABASE_URL"),
    )


def buscar(pergunta, vector_store=None, k=TOP_K):
    vector_store = vector_store or get_vector_store()
    return vector_store.similarity_search_with_score(pergunta, k=k)


def montar_contexto(resultados):
    return "\n\n".join(doc.page_content for doc, _score in resultados)


def montar_prompt(pergunta, resultados):
    contexto = montar_contexto(resultados)
    return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)


class SearchChain:
    """Encapsula a vector store para reuso por pergunta (chat.py chama .invoke por pergunta)."""

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def invoke(self, pergunta):
        resultados = buscar(pergunta, vector_store=self.vector_store)
        return montar_prompt(pergunta, resultados)

    __call__ = invoke


def search_prompt(question=None):
    try:
        vector_store = get_vector_store()
    except Exception:
        return None

    chain = SearchChain(vector_store)
    if question is None:
        return chain
    return chain.invoke(question)