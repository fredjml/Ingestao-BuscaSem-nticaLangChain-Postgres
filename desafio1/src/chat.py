import os

from dotenv import load_dotenv

from search import search_prompt

load_dotenv()

COMANDOS_SAIR = {"sair", "exit", "quit"}


def get_llm(provider=None):
    provider = (provider or os.getenv("EMBEDDING_PROVIDER", "openai")).lower()
    if provider in ("gemini", "google"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite"))

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano"))


def perguntar(pergunta, chain, llm=None):
    llm = llm or get_llm()
    prompt = chain.invoke(pergunta)
    resposta = llm.invoke(prompt)
    return getattr(resposta, "content", resposta)


def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    llm = get_llm()

    while True:
        pergunta = input("Faça sua pergunta: ").strip()

        if pergunta.lower() in COMANDOS_SAIR:
            break
        if not pergunta:
            continue

        resposta = perguntar(pergunta, chain, llm=llm)
        print(f"RESPOSTA: {resposta}")


if __name__ == "__main__":
    main()