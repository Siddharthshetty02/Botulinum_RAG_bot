import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def build_vector_store():
    print("1. Loading document...")
    # Load our sample document
    loader = TextLoader("data/sample_document.txt")
    documents = loader.load()

    print("2. Splitting document into chunks...")
    # Split the document into smaller chunks.
    # This is important so the LLM doesn't get overwhelmed with too much text,
    # and we only retrieve the most relevant pieces.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, 
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   Created {len(chunks)} chunks.")

    print("3. Initializing Embedding Model...")
    # We use a free, local HuggingFace model to turn text into vectors.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("4. Creating and saving Vector Store...")
    # We store the vectors in a local Chroma database.
    # The 'persist_directory' tells Chroma to save the data to disk so we can load it later.
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    
    print("Vector store built successfully in the './chroma_db' folder!")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    build_vector_store()
