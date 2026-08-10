import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def index_all_documents():
    print("1. Loading all documents from data/ directory...")
    data_dir = "data"
    all_chunks = []
    
    markdown_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    
    files = [f for f in os.listdir(data_dir) if f.endswith(('.md', '.txt'))]
    print(f"   Found {len(files)} text/markdown files to index: {files}")
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            
            if filename.endswith(".md"):
                chunks = markdown_splitter.split_documents(docs)
            else:
                chunks = text_splitter.split_documents(docs)
                
            all_chunks.extend(chunks)
            print(f"   - {filename}: created {len(chunks)} chunks.")
        except Exception as e:
            print(f"   - Error reading {filename}: {e}")

    print(f"\n2. Initializing Embedding Model ('all-MiniLM-L6-v2')...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("\n3. Indexing chunks into Chroma vector store ('./chroma_db')...")
    vector_store = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print("\nSuccessfully indexed all ML knowledge base documents into ChromaDB!")

if __name__ == "__main__":
    index_all_documents()
