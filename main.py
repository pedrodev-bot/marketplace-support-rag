import os
import chromadb
from groq import Groq
from dotenv import load_dotenv

# loads enviroment variables (security)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("ERROR: Groq API key not found in .env file.")

# initialize clients (vector database and LLM)
chroma_client = chromadb.PersistentClient(path="./banco_vetorial")
collection = chroma_client.get_or_create_collection(name="platform_rules_kb")
llm_client = Groq(api_key=api_key)

# rag function (main algorithm)
def ask_assistant(user_query: str) -> str:
    print("\n Searching for context in the vector database...")

    # semantic search
    results = collection.query(
        query_texts=[user_query],
        n_results=1
    )

    retrieved_context = results['documents'][0][0]
    print(f"Context found: '{retrieved_context}'")

    print("\n Sending context and query to the LLM...")

    # dynamic prompt engineering (content in pt-br)
    injected_prompt = f"""
    Você é um assistente de suporte a lojistas de um marketplace.
    Baseie a sua resposta EXCLUSIVAMENTE nas regras fornecidas abaixo. 
    Se a resposta não estiver nas regras, diga que não tem essa informação.
    
    REGRAS DA PLATAFORMA:
    {retrieved_context}
    
    PERGUNTA DO LOJISTA:
    {user_query}
    """

    # api call
    response = llm_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": injected_prompt}],
        temperature=0.0 # zero deterministic, no hallucinations
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("FoodTech Assistant Initialized! (type 'sair' to exit)")
    while True:
        user_input = input("\nLojista: ")

        if user_input.lower() == 'sair':
            break

        assistant_response = ask_assistant(user_input)

        print("\n ASSISTANT RESPONSE")
        print(assistant_response)
        print("\n")