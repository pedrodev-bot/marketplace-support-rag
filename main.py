import os
from groq import Groq

api_key = "api_groq"
client = Groq(api_key=api_key)

with open("faq_lojistas.txt", "r", encoding="utf-8") as f:
    texto_base = f.read()

pergunta = "Qual é a taxa de repasse do plano básico?"

prompt_injetado = f"Baseado estritamente nas regras abaixo:\n{texto_base}\n\nResponda à pergunta: {pergunta}"

print("Enviando para o LLM, aguarde...")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages =[
        {"role": "system", "content": "Você é um assistente virtual de suporte Nível 1 para lojistas de um marketplace de delivery. Responda de forma clara, objetiva e baseada estritamente nas regras de negócio fornecidas."},
        {"role": "user", "content": prompt_injetado}
    ],
    temperature=0.0
)

print("RESPOSTA DO BOT")
print(response.choices[0].message.content)