import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

embeddings = None
vector_store = None
llm = None
prompt_template = None

def initialize_rag_models():
    global embeddings, vector_store, llm, prompt_template
    print("Initializing RAG Pipeline models globally (this might take a few seconds)...")
    try:
        # We need to use the exact same embedding model that we used to build the store
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Load the existing database from disk
        vector_store = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=embeddings
        )
        
        # Initialize the OpenRouter model (requires OPENROUTER_API_KEY in .env)
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="openai/gpt-oss-20b:free"
        )
        
        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful assistant. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Context:
{context}

Question:
{question}

Answer:"""
        )
        print("Models initialized successfully!")
    except Exception as e:
        print(f"Warning: Failed to initialize models. Check your .env file or chroma_db directory. Error: {e}")

# Run initialization once on load
initialize_rag_models()


def query_rag(user_question):
    print(f"\nQuestion: {user_question}\n")
    print("1. Retrieving relevant context...")
    # Find the top 3 most similar chunks to the user's question
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(user_question)
    
    # Combine the retrieved text into a single string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    print(f"   Retrieved context length: {len(context)} characters")

    print("2. Generating answer using LLM...")
    
    # Format the prompt with our context and question
    final_prompt = prompt_template.format(context=context, question=user_question)
    
    # Ask the LLM
    response = llm.invoke(final_prompt)
    
    content = response.content
    if isinstance(content, list):
        # Extract text if the content is returned as a list of dicts (multimodal format)
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict) and "text" in part]
        content = "".join(text_parts) if text_parts else str(content)
        
    print("\n--- FINAL ANSWER ---")
    try:
        print(content)
    except UnicodeEncodeError:
        print(content.encode("ascii", "replace").decode("ascii"))
    print("--------------------\n")
    
    return content

if __name__ == "__main__":
    if not os.path.exists("./chroma_db"):
        print("Error: Vector store not found. Please run 1_build_vector_store.py first.")
    elif not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_api_key_here":
        print("Error: Missing OPENROUTER_API_KEY.")
        print("Please create a .env file, add your API key like in .env.example, and try again.")
    else:
        # Test questions
        question1 = "What is the name of the proprietary algorithm used in Physio_AI?"
        query_rag(question1)
        
        question2 = "Who is the lead researcher on the project?"
        query_rag(question2)
