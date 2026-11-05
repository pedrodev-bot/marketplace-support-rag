import chromadb

chroma_client = chromadb.PersistentClient(path="./banco_vetorial")

collection = chroma_client.get_or_create_collection(name="platform_rules_kb")

chunks_de_texto = [
    "A taxa de repasse da plataforma para o plano Básico é de 12% sobre o valor bruto do pedido.",
    "O repasse financeiro para os lojistas parceiros ocorre toda quarta-feira via PIX ou TED.",
    "Lojistas com avaliação média inferior a 3.5 perdem o selo de Destaque e sofrem redução no algoritmo de visibilidade."
]

ids_dos_chunks = ["bloco_1", "bloco_2", "bloco_3"]

print("Gerando vetores e salvando no banco...")
collection.upsert(
    documents=chunks_de_texto,
    ids=ids_dos_chunks
)

pergunta_do_usuario = "Que dia cai o dinheiro na minha conta?"
print(f"\nBuscando a resposta para: '{pergunta_do_usuario}'")

resultados = collection.query(
    query_texts=[pergunta_do_usuario],
    n_results=1
)

print("\n--- TEXTO ENCONTRADO PELO BANCO VETORIAL ---")
print(resultados['documents'][0][0])