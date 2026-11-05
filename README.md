# FoodTech Partner Copilot 🍔🤖

Proof of Concept (PoC) for a Retrieval-Augmented Generation (RAG) system designed to reduce Level 1 support overhead in delivery marketplaces (FoodTechs). 

This assistant resolves complex partner inquiries (e.g., fee structures, visibility algorithms, and financial payouts) by autonomously querying internal knowledge bases and operational manuals.

## 🎯 The Business Problem
Delivery platforms in hypergrowth handle thousands of partner support tickets daily. Generic LLMs tend to hallucinate fees and rules, causing compliance issues. This solution leverages RAG to ensure the AI generates responses **strictly grounded in official platform documentation**, combining the conversational fluidity of Generative AI with the precision of deterministic business logic.

## 🏗️ Architecture & Tech Stack
- **LLM / Generation Engine:** openai/gpt-oss-120b (via Groq API for ultra-low latency inference).
- **Vector Database:** ChromaDB (Local storage and spatial indexing).
- **Embeddings:** `sentence-transformers` (Open-source models for semantic similarity calculations).
- **Language:** Python.

## 🚀 Current Status (Phase 1 - Core Backend)
- [x] Asynchronous LLM integration with strict temperature parametrization to prevent hallucinations (Zero-shot deterministic).
- [x] Local vector database (ChromaDB) modeling and text embedding ingestion routines.
- [x] Semantic search implementation for intelligent context retrieval (K-Nearest Neighbors).

## ⏭️ Architectural Roadmap (Phase 2)
- [ ] **Integration:** Merge the retrieval script (VectorDB) with the inference engine (LLM) into a unified pipeline.
- [ ] **Microservices:** Wrap the RAG pipeline into an asynchronous RESTful API using **FastAPI**.
- [ ] **Deployment:** Containerize and serve the application via Hugging Face Spaces using a Gradio/Streamlit frontend.