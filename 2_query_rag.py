import os
import re
import sys
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Reconfigure stdout for Windows console UTF-8 safety
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Load environment variables from .env file
load_dotenv()


embeddings = None
vector_store = None
llm = None
prompt_template = None

# Fast-path pattern matcher for simple greetings and casual questions
GREETINGS_MAP = {
    r"^(hi|hello|hey|hola|heyy+|hii+|greetings|howdy)[\s!.]*$": "Hello! I am Botulinum Bot, your Neural RAG Studio assistant. How can I help you today with your documents or Machine Learning questions?",
    r"^(how are you|how are you\?|how\'s it going|how do you do)[\s!.]*$": "I'm doing great and ready to answer any questions about your uploaded documents or Machine Learning topics!",
    r"^(who are you|what is your name|what are you|who created you)[\s!.]*$": "I am Botulinum Bot, a Neural RAG Studio assistant powered by OpenRouter LLMs, ChromaDB, and an Artificial Neural Network visualizer.",
    r"^(thanks|thank you|thx|thank you so much|thanks!)[\s!.]*$": "You're very welcome! Feel free to ask if you have any more questions.",
    r"^(bye|goodbye|cya|see ya)[\s!.]*$": "Goodbye! Have a fantastic day ahead!",
    r"^(what can you do|help|features|what is this)[\s!.]*$": "I can analyze and answer questions from your uploaded PDF/Markdown documents, explain Machine Learning concepts, search ChromaDB vector embeddings, and visualize neural activations!"
}

def check_fast_path_greeting(question):
    cleaned = question.strip().lower()
    for pattern, response in GREETINGS_MAP.items():
        if re.search(pattern, cleaned):
            return response
    return None

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
            template="""You are a world-class Senior AI/ML Staff Engineer and friendly Mentor explaining engineering & Machine Learning concepts to junior developers.

Persona & Style:
- Explain technical concepts with accuracy, using clear real-world analogies where helpful.
- Speak like an encouraging, expert senior mentor guiding a teammate.

Formatting Rules:
- Mandatory: ALWAYS format long or detailed answers into clear, structured bullet points or numbered lists. Never return a long solid block of text.
- Use bold formatting (**term**) to emphasize key terms, headings, and core takeaways. Do NOT use quotation marks for bolding.
- Base your technical answers on the retrieved context below. If the context does not contain enough information, state that clearly.

Context:
{context}

Question:
{question}

Senior ML Engineer Answer:"""
        )
        print("Models initialized successfully!")
    except Exception as e:
        print(f"Warning: Failed to initialize models. Check your .env file or chroma_db directory. Error: {e}")

# Run initialization once on load
initialize_rag_models()


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))

def get_rl_reward_weights():
    if os.path.exists("rl_rewards.json"):
        try:
            with open("rl_rewards.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("chunk_rewards", {})
        except Exception:
            pass
    return {}

def retrieve_rl_augmented_context(user_question, k=3):
    chunk_rewards = get_rl_reward_weights()
    
    try:
        # Retrieve top k*2 candidate chunks to re-rank with RL rewards
        raw_results = vector_store.similarity_search_with_score(user_question, k=k*2)
        scored_docs = []
        
        for doc, dist in raw_results:
            similarity = 1.0 / (1.0 + float(dist))
            words = [w.lower() for w in doc.page_content.split() if len(w) > 3]
            rl_boost = sum(chunk_rewards.get(w, 0.0) for w in words) if chunk_rewards else 0.0
            
            final_score = similarity + (0.15 * rl_boost)
            scored_docs.append((doc, final_score))
            
        scored_docs.sort(key=lambda item: item[1], reverse=True)
        return [doc for doc, score in scored_docs[:k]]
    except Exception as e:
        safe_print(f"Fallback to default retriever: {e}")
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(user_question)

def query_rag(user_question):
    safe_print(f"\nQuestion: {user_question}\n")
    
    # Fast path for simple greetings and casual questions
    fast_response = check_fast_path_greeting(user_question)
    if fast_response:
        safe_print("[Fast Path] Handled simple greeting/query instantly without RAG retrieval or API delay.")
        return {"answer": fast_response, "is_fast_path": True}

    safe_print("1. Retrieving relevant context with RL Reward Re-ranking...")
    retrieved_docs = retrieve_rl_augmented_context(user_question, k=3)
    
    # Combine the retrieved text into a single string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    safe_print(f"   Retrieved context length: {len(context)} characters")

    safe_print("2. Generating answer using LLM...")
    
    # Format the prompt with our context and question
    final_prompt = prompt_template.format(context=context, question=user_question)
    
    # Ask the LLM
    response = llm.invoke(final_prompt)
    
    content = response.content
    if isinstance(content, list):
        # Extract text if the content is returned as a list of dicts (multimodal format)
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict) and "text" in part]
        content = "".join(text_parts) if text_parts else str(content)
        
    safe_print("\n--- FINAL ANSWER ---")
    safe_print(content)
    safe_print("--------------------\n")
    
    return {"answer": content, "is_fast_path": False}

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
