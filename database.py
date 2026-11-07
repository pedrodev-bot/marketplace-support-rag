import os
import chromadb

# initialize Vector Database
chroma_client = chromadb.PersistentClient(path="./banco_vetorial")
collection = chroma_client.get_or_create_collection(name="platform_rules_kb")

# extract: Read the external Knowledge Base file
file_path = "faq_lojistas.txt"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"CRITICAL: Knowledge base file '{file_path}' not found.")

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# chunk the text (splitting by newlines and removing empty lines)
text_chunks = [line.strip() for line in content.split('\n') if line.strip()]

# generate sequential unique IDs for the chunks
chunk_ids = [f"rule_chunk_{i}" for i in range(len(text_chunks))]

# load upsert into ChromaDB
print(f"🔄 Ingesting {len(text_chunks)} rules into the vector database...")

collection.upsert(
    documents=text_chunks,
    ids=chunk_ids
)

print("✅ Data ingestion complete! The knowledge base is updated.")