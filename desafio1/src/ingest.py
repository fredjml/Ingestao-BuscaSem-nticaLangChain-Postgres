import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_documents(pdf_path):
    return PyPDFLoader(pdf_path).load()


def split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def get_embeddings(provider=None):
    provider = (provider or os.getenv("EMBEDDING_PROVIDER", "openai")).lower()
    if provider in ("gemini", "google"):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))


def collection_name_for(provider=None, base=None):
    provider = (provider or os.getenv("EMBEDDING_PROVIDER", "openai")).lower()
    base = base or os.getenv("PG_VECTOR_COLLECTION_NAME", "desafio1")
    return f"{base}_{provider}"


def build_vector_store(documents, embeddings, collection_name, connection=None):
    connection = connection or os.getenv("DATABASE_URL")
    return PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        connection=connection,
        collection_name=collection_name,
        pre_delete_collection=True,  # DEC-06: idempotencia (drop/create a cada ingestao)
    )


def ingest_pdf():
    pdf_path = os.getenv("PDF_PATH", "./document.pdf")
    database_url = os.getenv("DATABASE_URL")

    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF_PATH invalido ou arquivo nao encontrado: {pdf_path}")
    if not database_url:
        raise RuntimeError("DATABASE_URL nao configurado (.env)")

    documents = load_documents(pdf_path)
    chunks = split_documents(documents)
    embeddings = get_embeddings()
    collection = collection_name_for()
    build_vector_store(chunks, embeddings, collection, connection=database_url)

    print(f"Ingestao concluida: {len(chunks)} chunks indexados na colecao '{collection}'.")
    return len(chunks)


if __name__ == "__main__":
    ingest_pdf()