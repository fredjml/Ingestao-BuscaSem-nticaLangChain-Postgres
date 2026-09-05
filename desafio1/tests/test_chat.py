from unittest.mock import MagicMock

import chat


def test_get_llm_openai_default(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from langchain_openai import ChatOpenAI

    assert isinstance(chat.get_llm(), ChatOpenAI)


def test_get_llm_gemini(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    from langchain_google_genai import ChatGoogleGenerativeAI

    assert isinstance(chat.get_llm(provider="gemini"), ChatGoogleGenerativeAI)


def test_perguntar_invoca_chain_e_llm_retorna_content():
    fake_chain = MagicMock()
    fake_chain.invoke.return_value = "PROMPT MONTADO"

    fake_resposta = MagicMock()
    fake_resposta.content = "O faturamento foi de 10 milhões de reais."
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = fake_resposta

    resultado = chat.perguntar("Qual o faturamento?", fake_chain, llm=fake_llm)

    fake_chain.invoke.assert_called_once_with("Qual o faturamento?")
    fake_llm.invoke.assert_called_once_with("PROMPT MONTADO")
    assert resultado == "O faturamento foi de 10 milhões de reais."


def test_perguntar_repassa_fallback_exato_sem_alterar():
    fallback = "Não tenho informações necessárias para responder sua pergunta."
    fake_chain = MagicMock()
    fake_chain.invoke.return_value = "PROMPT COM CONTEXTO VAZIO"

    fake_resposta = MagicMock()
    fake_resposta.content = fallback
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = fake_resposta

    resultado = chat.perguntar("Quantos clientes temos em 2024?", fake_chain, llm=fake_llm)

    assert resultado == fallback


def test_main_encerra_se_chain_none(monkeypatch, capsys):
    monkeypatch.setattr(chat, "search_prompt", lambda: None)

    chat.main()

    saida = capsys.readouterr().out
    assert "Não foi possível iniciar o chat" in saida


def test_main_sai_com_comando_sair(monkeypatch):
    fake_chain = MagicMock()
    monkeypatch.setattr(chat, "search_prompt", lambda: fake_chain)
    monkeypatch.setattr(chat, "get_llm", lambda: MagicMock())
    monkeypatch.setattr("builtins.input", lambda _: "sair")

    perguntar_chamado = MagicMock()
    monkeypatch.setattr(chat, "perguntar", perguntar_chamado)

    chat.main()

    perguntar_chamado.assert_not_called()


def test_main_pergunta_e_imprime_resposta(monkeypatch, capsys):
    fake_chain = MagicMock()
    monkeypatch.setattr(chat, "search_prompt", lambda: fake_chain)
    monkeypatch.setattr(chat, "get_llm", lambda: MagicMock())

    entradas = iter(["Qual o faturamento?", "sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    monkeypatch.setattr(chat, "perguntar", lambda pergunta, chain, llm=None: "O faturamento foi de 10 milhões.")

    chat.main()

    saida = capsys.readouterr().out
    assert "RESPOSTA: O faturamento foi de 10 milhões." in saida
