import os
from unittest.mock import MagicMock

import pytest
from langchain_core.documents import Document

import ingest


def test_split_documents_uses_1000_150(monkeypatch):
    captured = {}

    class FakeSplitter:
        def __init__(self, chunk_size, chunk_overlap):
            captured["chunk_size"] = chunk_size
            captured["chunk_overlap"] = chunk_overlap

        def split_documents(self, documents):
            return documents

    monkeypatch.setattr(ingest, "RecursiveCharacterTextSplitter", FakeSplitter)

    result = ingest.split_documents([Document(page_content="conteudo")])

    assert captured == {"chunk_size": 1000, "chunk_overlap": 150}
    assert result == [Document(page_content="conteudo")]


def test_get_embeddings_openai_default(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from langchain_openai import OpenAIEmbeddings

    assert isinstance(ingest.get_embeddings(), OpenAIEmbeddings)


def test_get_embeddings_gemini(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    assert isinstance(ingest.get_embeddings(provider="gemini"), GoogleGenerativeAIEmbeddings)


def test_collection_name_for_includes_provider():
    assert ingest.collection_name_for(provider="openai", base="desafio1") == "desafio1_openai"
    assert ingest.collection_name_for(provider="gemini", base="desafio1") == "desafio1_gemini"


def test_build_vector_store_uses_pre_delete_collection(monkeypatch):
    fake_store = MagicMock()
    fake_from_documents = MagicMock(return_value=fake_store)
    monkeypatch.setattr(ingest.PGVector, "from_documents", fake_from_documents)

    result = ingest.build_vector_store(
        [Document(page_content="x")],
        MagicMock(),
        "desafio1_openai",
        connection="postgresql://x",
    )

    assert result is fake_store
    _, kwargs = fake_from_documents.call_args
    assert kwargs["pre_delete_collection"] is True  # DEC-06: idempotencia (drop/create)
    assert kwargs["collection_name"] == "desafio1_openai"
    assert kwargs["connection"] == "postgresql://x"


def test_ingest_pdf_raises_without_pdf(monkeypatch):
    monkeypatch.setenv("PDF_PATH", "arquivo-que-nao-existe.pdf")
    monkeypatch.setenv("DATABASE_URL", "postgresql://x")

    with pytest.raises(FileNotFoundError):
        ingest.ingest_pdf()


def test_ingest_pdf_raises_without_database_url(monkeypatch):
    monkeypatch.setenv("PDF_PATH", "document.pdf")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError):
        ingest.ingest_pdf()


def test_ingest_pdf_orchestrates_pipeline(monkeypatch):
    monkeypatch.setenv("PDF_PATH", "document.pdf")
    monkeypatch.setenv("DATABASE_URL", "postgresql://x")
    monkeypatch.setenv("PG_VECTOR_COLLECTION_NAME", "desafio1")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")

    fake_chunks = [Document(page_content="a1"), Document(page_content="a2")]

    monkeypatch.setattr(ingest, "load_documents", lambda path: [Document(page_content="a")])
    monkeypatch.setattr(ingest, "split_documents", lambda docs: fake_chunks)
    monkeypatch.setattr(ingest, "get_embeddings", lambda: MagicMock())
    monkeypatch.setattr(
        ingest, "build_vector_store", lambda chunks, emb, coll, connection=None: MagicMock()
    )
    monkeypatch.setattr(os.path, "exists", lambda p: True)

    assert ingest.ingest_pdf() == 2
