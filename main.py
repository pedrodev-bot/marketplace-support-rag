import os
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

# fastapi initialization
app = FastAPI(
    title="FoodTech Partner Copilot API",
    description="RAG-powered support API for marketplace partners",
    version="1.0.0"
)

# data validation schema
class SupportRequest(BaseModel):
    user_query: str

class SupportResponse(BaseModel):
    answer: str
    source_context: str

# rag function (main algorithm and api endpoint)
@app.post("/api/v1/ask", response_model=SupportResponse)
async def ask_assistant(request: SupportRequest):
    try:
        # semantic search
        results = collection.query(
            query_texts=[request.user_query],
            n_results=1
        )

        # check if context was found
        if not results['documents'] or not results['documents'][0]:
            raise HTTPException(status_code=404, detail="No relevant context found in the knowledge base.")

        retrieved_context = results['documents'][0][0]

        # prompt engineering (content in pt-br)
        injected_prompt = f"""
        Você é um assistente de suporte a lojistas de um marketplace.
        Baseie a sua resposta EXCLUSIVAMENTE nas regras fornecidas abaixo. 
        Se a resposta não estiver nas regras, diga que não tem essa informação.
        
        REGRAS DA PLATAFORMA:
        {retrieved_context}
        
        PERGUNTA DO LOJISTA:
        {request.user_query}
        """

        # llm inference
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": injected_prompt}],
            temperature=0.0 # zero deterministic, no hallucinations
        )

        return SupportResponse(
            answer=str(response.choices[0].message.content),
            source_context=retrieved_context
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))