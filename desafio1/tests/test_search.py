from unittest.mock import MagicMock

from langchain_core.documents import Document

import search


def test_montar_contexto_concatena_page_content():
    resultados = [
        (Document(page_content="chunk um"), 0.1),
        (Document(page_content="chunk dois"), 0.2),
    ]

    contexto = search.montar_contexto(resultados)

    assert "chunk um" in contexto
    assert "chunk dois" in contexto


def test_montar_prompt_usa_template_com_contexto_e_pergunta():
    resultados = [(Document(page_content="fato relevante"), 0.1)]

    prompt = search.montar_prompt("Qual o faturamento?", resultados)

    assert "fato relevante" in prompt
    assert "Qual o faturamento?" in prompt
    assert "Não tenho informações necessárias para responder sua pergunta." in prompt
    assert "RESPONDA A \"PERGUNTA DO USUÁRIO\"" in prompt


def test_buscar_chama_similarity_search_with_score_k10():
    fake_store = MagicMock()
    fake_store.similarity_search_with_score.return_value = [(Document(page_content="x"), 0.5)]

    resultado = search.buscar("pergunta", vector_store=fake_store)

    fake_store.similarity_search_with_score.assert_called_once_with("pergunta", k=10)
    assert resultado == [(Document(page_content="x"), 0.5)]


def test_get_vector_store_usa_mesmo_provider_da_ingestao(monkeypatch):
    fake_embeddings = MagicMock()
    fake_pgvector_instance = MagicMock()
    fake_pgvector_cls = MagicMock(return_value=fake_pgvector_instance)

    monkeypatch.setattr(search, "get_embeddings", lambda: fake_embeddings)
    monkeypatch.setattr(search, "collection_name_for", lambda: "desafio1_openai")
    monkeypatch.setattr(search, "PGVector", fake_pgvector_cls)
    monkeypatch.setenv("DATABASE_URL", "postgresql://x")

    result = search.get_vector_store()

    assert result is fake_pgvector_instance
    _, kwargs = fake_pgvector_cls.call_args
    assert kwargs["embeddings"] is fake_embeddings
    assert kwargs["collection_name"] == "desafio1_openai"
    assert kwargs["connection"] == "postgresql://x"


def test_search_chain_invoke_monta_prompt_a_partir_dos_resultados(monkeypatch):
    fake_store = MagicMock()
    chain = search.SearchChain(fake_store)

    monkeypatch.setattr(
        search, "buscar", lambda pergunta, vector_store=None, k=10: [(Document(page_content="dado"), 0.1)]
    )

    prompt = chain.invoke("pergunta do usuario")

    assert "dado" in prompt
    assert "pergunta do usuario" in prompt


def test_search_prompt_sem_pergunta_retorna_chain(monkeypatch):
    monkeypatch.setattr(search, "get_vector_store", lambda: MagicMock())

    chain = search.search_prompt()

    assert chain is not None
    assert hasattr(chain, "invoke")


def test_search_prompt_com_pergunta_retorna_prompt_final(monkeypatch):
    monkeypatch.setattr(search, "get_vector_store", lambda: MagicMock())
    monkeypatch.setattr(
        search, "buscar", lambda pergunta, vector_store=None, k=10: [(Document(page_content="dado"), 0.1)]
    )

    resultado = search.search_prompt("minha pergunta")

    assert "dado" in resultado
    assert "minha pergunta" in resultado


def test_search_prompt_retorna_none_se_inicializacao_falhar(monkeypatch):
    def boom():
        raise RuntimeError("sem conexao")

    monkeypatch.setattr(search, "get_vector_store", boom)

    assert search.search_prompt() is None
