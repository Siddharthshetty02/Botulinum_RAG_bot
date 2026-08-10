# Retrieval-Augmented Generation (RAG) & Vector Databases

## 1. RAG Architecture Overview

Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs) by grounding generation on external knowledge retrieved dynamically from a domain-specific vector database or search index.

### 1.1 Core RAG Pipeline Components
1. **Document Ingestion & Parsing**: Extracting raw text from documents (PDFs, Markdown, Web pages, HTML).
2. **Text Chunking**: Breaking documents into smaller, semantic chunks (e.g., 200–500 tokens) with overlap (e.g., 50 tokens) to preserve context boundaries.
3. **Embedding Generation**: Converting text chunks into high-dimensional numerical vectors using dense embedding models (e.g., `all-MiniLM-L6-v2`, `text-embedding-3-small`, `bge-large-en`).
4. **Vector Indexing & Storage**: Saving vectors into specialized Vector Databases (ChromaDB, FAISS, Pinecone, Qdrant, Milvus, Weaviate).
5. **Similarity Retrieval**: Querying the vector store with user question embeddings using distance metrics (Cosine Similarity, Euclidean Distance, Dot Product).
6. **Prompt Assembly & LLM Generation**: Augmenting the user's prompt with retrieved context chunks before passing to the LLM (e.g., GPT-4, Llama-3, OpenRouter models) for response synthesis.

---

## 2. Mathematical Vector Search Metrics

For query vector $\mathbf{q}$ and document chunk vector $\mathbf{d}$:

- **Cosine Similarity**: Measures angle between vectors regardless of magnitude.
  $$\text{Cosine}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|} = \frac{\sum q_i d_i}{\sqrt{\sum q_i^2} \sqrt{\sum d_i^2}}$$
- **Euclidean Distance ($L_2$ Distance)**: Measures straight-line distance between vector endpoints.
  $$D_{L2}(\mathbf{q}, \mathbf{d}) = \sqrt{\sum_{i=1}^n (q_i - d_i)^2}$$
- **Dot Product**: Equivalent to Cosine Similarity when vectors are normalized to unit length ($L_2$ norm = 1).

---

## 3. Advanced RAG Techniques

### 3.1 Hybrid Search
Combines **Dense Retrieval** (semantic vector embeddings) with **Sparse Retrieval** (keyword BM25 / TF-IDF) to capture both semantic intent and exact keyphrase matches.

### 3.2 Context Reranking
Uses Cross-Encoder models (e.g., `bge-reranker-large`, Cohere Rerank) to re-order initial top-$K$ candidate retrieved chunks by fine-grained relevancy scores before injecting into the LLM context window.

### 3.3 GraphRAG & HyDE
- **HyDE (Hypothetical Document Embeddings)**: Generates a hypothetical answer using the LLM first, embeds the answer, and uses it to retrieve actual matching documents from vector storage.
- **GraphRAG**: Combines knowledge graphs (entities and relationship edges) with vector stores for global reasoning across large document corpora.
