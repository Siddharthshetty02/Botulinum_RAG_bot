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
    r"^(thanks|thank you|thx|thank you so much|thanks!)[\s!.]*$": "You're very welcome! Feel free to ask if you have any more questions.",
    r"^(bye|goodbye|cya|see ya)[\s!.]*$": "Goodbye! Have a fantastic day ahead!",
    r"^(what can you do|help|features|what is this)[\s!.]*$": "I can analyze and answer questions from your uploaded PDF/Markdown documents, explain Machine Learning concepts, search ChromaDB vector embeddings, and visualize neural activations!"
}

# Creator verification state map (stores active challenge per session/query pattern)
CREATOR_CHALLENGE_STATE = {"challenged": False}

# Patterns to match questions about the creator/developer
CREATOR_PATTERNS = [
    r"who created you", r"who made you", r"who is your creator", r"who is your developer",
    r"who built you", r"who is your owner", r"who designed you", r"tell me about your creator",
    r"who created this", r"who is the creator"
]

def check_creator_challenge(question):
    cleaned = question.strip().lower()
    
    # 1. Check if user is asking who created the bot
    if any(re.search(pat, cleaned) for pat in CREATOR_PATTERNS):
        CREATOR_CHALLENGE_STATE["challenged"] = True
        return "I was created by an AI/ML Software Engineer! To unlock detailed information about my creator, please answer this security question: **Which is his favorite cricketer?**"
        
    # 2. If challenged state is active, check answer
    if CREATOR_CHALLENGE_STATE["challenged"]:
        if "ms dhoni" in cleaned or "dhoni" in cleaned or "mahendra singh dhoni" in cleaned or "msd" in cleaned:
            CREATOR_CHALLENGE_STATE["challenged"] = False
            return ("Verification successful! 🏏 Here is the profile of my creator:\n\n"
                    "**Siddharth Shetty** is a 4th-year Computer Science and Engineering student at **AMC Engineering College** (affiliated with Visvesvaraya Technological University / VTU).\n\n"
                    "**Key Highlights & Profile**:\n"
                    "- **Technical Focus**: Artificial Intelligence, Machine Learning, Software Engineering, RAG & LLM Application Engineering, and Embedded Systems.\n"
                    "- **Tech Stack**: Python, Data Structures & Algorithms (DSA), XGBoost, ESP32, MPU6050, Bluetooth Low Energy (BLE), Android Development, and LLM-based apps.\n"
                    "- **Key Projects**:\n"
                    "  1. **IoT-Based Intelligent Physiotherapy Monitoring & Real-Time Feedback System**: Built with ESP32, MPU6050, and BLE for motion analysis and posture feedback.\n"
                    "  2. **CarbonWise**: An intelligent carbon-footprint tracking application to calculate and optimize environmental impact.\n"
                    "- **Activities & Achievements**: Active participant in Hackathons, Prompt Wars, Google Developer Student Club (GDSC) activities, and open-source projects while building his GitHub & LinkedIn portfolio.\n"
                    "- **Current Focus**: Preparing for **GATE 2027** and developing strong problem-solving and practical engineering skills for placements and internships.")
        else:
            CREATOR_CHALLENGE_STATE["challenged"] = False
            return "Nope!"
            
    return None

# Political guardrail topics & keywords
POLITICAL_PATTERNS = [
    r"\b(politics|political|politician|politicians|election|elections|voting|ballot|campaign)\b",
    r"\b(democrat|democrats|republican|republicans|parliament|congressman|senator|governor)\b",
    r"\b(president|prime minister|head of state|political party|left-wing|right-wing|partisan)\b",
    r"\b(trump|biden|obama|modi|putin|xi jinping|starmer|kamala|vance)\b",
    r"\b(government policy opinion|foreign policy debate|geopolitics|political scandal)\b"
]

# Specific RCB & Virat Kohli guardrail patterns (only targeting RCB & Virat Kohli)
RCB_PATTERNS = [
    r"\b(rcb|royal challengers|royal challengers bangalore|play bold|ee sala cup namde)\b",
    r"\b(virat|kohli|virat kohli)\b"
]

def check_political_guardrail(question):
    """
    POLITICAL GUARDRAIL CHECK:
    Why it was added: Prevents off-topic political, election, or partisan queries from reaching
    the LLM or spending vector store resources. Enforces strict domain boundaries on AI/ML.
    Returns guardrail notice string if political query detected, else None.
    """
    cleaned = question.strip().lower()
    if any(re.search(pat, cleaned) for pat in POLITICAL_PATTERNS):
        return ("⚠️ **Guardrail Notice**: As a specialized Machine Learning & Technical RAG Assistant, "
                "I am programmed to decline political, election, or partisan opinion questions. "
                "Please feel free to ask any question regarding **Machine Learning**, **AI algorithms**, "
                "**Data Science**, or your **uploaded documents**!")
    return None

def check_cricket_and_rcb_guardrail(question):
    """
    STRICT RCB & VIRAT KOHLI GUARDRAIL CHECK:
    Why it was added: User explicitly requested restricting ONLY RCB (Royal Challengers Bangalore) 
    and Virat Kohli queries, while leaving all other questions unrestricted.
    """
    cleaned = question.strip().lower()
    
    if any(re.search(pat, cleaned) for pat in RCB_PATTERNS):
        return ("🚫 **Guardrail Blocked**: I am programmed to strictly decline questions about **RCB (Royal Challengers Bangalore)** "
                "and **Virat Kohli**. As a specialized Machine Learning Assistant, "
                "I focus on **Machine Learning**, **Data Science**, **AI Engineering**, and your **uploaded documents**.")
    return None

def check_fast_path_greeting(question):
    # 1. Check political guardrails
    pol_response = check_political_guardrail(question)
    if pol_response:
        return pol_response

    # 2. Check Virat Kohli & RCB cricket guardrails
    cricket_response = check_cricket_and_rcb_guardrail(question)
    if cricket_response:
        return cricket_response

    # 3. Check creator verification challenge
    creator_response = check_creator_challenge(question)
    if creator_response:
        return creator_response

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
        
        # Initialize the OpenRouter model with Nemotron Ultra (requires OPENROUTER_API_KEY in .env)
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="nvidia/llama-3.1-nemotron-70b-instruct"
        )
        
        # Define fine-tuned Moderate-Length Machine Learning prompt template with examples
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a Fine-Tuned Machine Learning (ML) Specialist.

Your Role & Core Objective:
- Provide clear, well-structured, moderate-length Machine Learning explanations.
- Always include a practical REAL-WORLD EXAMPLE (e.g., predicting house prices, email spam detection, medical diagnosis, etc.) to clearly illustrate the concept.

Response Structure Guidelines:
- Keep your answer MODERATE in length (neither too short/cut-to-cut nor overly wordy).
- 1. **Concept Definition**: Explain the ML concept clearly and directly.
- 2. **Real-World Example**: Illustrate the concept with a concise, practical example.
- 3. **Key Highlights / Parameters**: List key parameters or core benefits using brief bullet points.

Safety & Guardrail Directives:
- Decline all political, partisan, or election-related questions politely in 1 short sentence.

Context:
{context}

Question:
{question}

ML Explanation & Example:"""
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
    # Fine-tuned default ML keyword weights if file does not exist yet
    return {
        "machine": 0.8, "learning": 0.8, "xgboost": 0.9, "hyperparameter": 0.85,
        "classification": 0.75, "regression": 0.75, "clustering": 0.75,
        "overfitting": 0.8, "bias": 0.8, "variance": 0.8, "validation": 0.7,
        "precision": 0.75, "recall": 0.75, "f1": 0.75, "chromadb": 0.7, "vector": 0.7
    }

def retrieve_rl_augmented_context(user_question, k=3):
    """
    RL-AUGMENTED CONTEXT RETRIEVAL & RE-RANKING:
    Why it was added: Standard vector similarity (cosine distance) can sometimes retrieve 
    sub-optimal chunks if phrasing differs. This module re-ranks candidate chunks by combining
    vector similarity with learned RL reward weights (from user 👍/👎 feedback) and ML domain priority keyword boosts.
    Also filters out personal creator profile context for general technical algorithm queries.
    """
    chunk_rewards = get_rl_reward_weights()
    cleaned_q = user_question.lower()
    is_creator_query = any(w in cleaned_q for w in ["creator", "developer", "made you", "built you", "siddharth", "who created"])
    
    try:
        # Retrieve top k*3 candidate chunks to re-rank with fine-tuned ML RL rewards
        raw_results = vector_store.similarity_search_with_score(user_question, k=k*3)
        scored_docs = []
        
        # High-priority ML domain keywords to boost during retrieval
        ml_priority_keywords = {
            "machine", "learning", "model", "algorithm", "hyperparameter", "accuracy",
            "precision", "recall", "f1", "xgboost", "validation", "cross-validation",
            "overfitting", "underfitting", "bias", "variance", "regularization", "loss",
            "feature", "vector", "embedding", "chromadb", "rag", "retrieval", "boosting"
        }
        
        for doc, dist in raw_results:
            source_file = doc.metadata.get("source", "").lower()
            
            # If not explicitly a creator query, skip creator profile chunks to avoid polluting technical explanations
            if not is_creator_query and ("creator" in source_file or "siddharth" in source_file):
                continue
                
            similarity = 1.0 / (1.0 + float(dist))
            words = [w.lower() for w in doc.page_content.split() if len(w) > 3]
            
            # Compute RL weight boost
            rl_boost = sum(chunk_rewards.get(w, 0.0) for w in words) if chunk_rewards else 0.0
            
            # Domain priority boost for core ML terms
            domain_boost = sum(0.1 for w in set(words) if w in ml_priority_keywords)
            
            final_score = similarity + (0.2 * rl_boost) + (0.1 * domain_boost)
            scored_docs.append((doc, final_score))
            
        scored_docs.sort(key=lambda item: item[1], reverse=True)
        return [doc for doc, score in scored_docs[:k]]
    except Exception as e:
        safe_print(f"Fallback to default retriever: {e}")
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(user_question)

# Ultra-fast OpenRouter models with high-speed priority fallback chain
FAST_MODELS = [
    "meta-llama/llama-3.3-70b-instruct",
    "qwen/qwen-2.5-coder-32b-instruct",
    "google/gemini-2.0-flash-001",
    "mistralai/mistral-small-24b-instruct-2501"
]

def invoke_llm_with_fast_fallback(final_prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY in environment variables.")

    import time
    start_time = time.time()
    
    last_exception = None
    for model_name in FAST_MODELS:
        try:
            safe_print(f"   [LLM Speed Engine] Querying {model_name} (timeout=10s)...")
            temp_llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model_name,
                timeout=10,
                max_tokens=600,
                max_retries=1
            )
            response = temp_llm.invoke(final_prompt)
            elapsed = time.time() - start_time
            safe_print(f"   ⚡ Response received from {model_name} in {elapsed:.2f} seconds!")
            return response
        except Exception as e:
            safe_print(f"   ⚠️ {model_name} delayed or failed ({e}). Failover to next fast model...")
            last_exception = e
            
    # Fallback to global default llm if loop completes
    return llm.invoke(final_prompt)

def query_rag(user_question):
    safe_print(f"\nQuestion: {user_question}\n")
    
    # Fast path for simple greetings, creator queries, and political guardrails
    fast_response = check_fast_path_greeting(user_question)
    if fast_response:
        safe_print("[Fast Path] Handled simple query instantly (0ms latency).")
        return {"answer": fast_response, "is_fast_path": True}

    safe_print("1. Retrieving relevant context with RL Reward Re-ranking...")
    retrieved_docs = retrieve_rl_augmented_context(user_question, k=3)
    
    # Combine the retrieved text into a single string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    safe_print(f"   Retrieved context length: {len(context)} characters")

    safe_print("2. Generating answer using Low-Latency LLM Fallback Engine...")
    
    # Format the prompt with context and question
    final_prompt = prompt_template.format(context=context, question=user_question)
    
    # Ask the LLM using low-latency fallback engine
    response = invoke_llm_with_fast_fallback(final_prompt)
    
    content = response.content
    if isinstance(content, list):
        # Extract text if returned as list of dicts
        text_parts = [part.get("text", "") for part in content if isinstance(part, dict) and "text" in part]
        content = "".join(text_parts) if text_parts else str(content)
        
    safe_print("\n--- FINAL ANSWER ---")
    safe_print(content)
    safe_print("--------------------\n")
    
    return {"answer": content, "is_fast_path": False}

def query_rag_stream(user_question):
    """
    Generator yielding token chunks word-by-word in real time for ultra-low perceived latency.
    """
    fast_response = check_fast_path_greeting(user_question)
    if fast_response:
        # Fast path token simulation
        words = fast_response.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
        return

    retrieved_docs = retrieve_rl_augmented_context(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    final_prompt = prompt_template.format(context=context, question=user_question)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        yield "Error: OPENROUTER_API_KEY is missing."
        return

    streamed_tokens = False
    for model_name in FAST_MODELS:
        try:
            safe_print(f"   [Streaming Engine] Connecting to {model_name}...")
            temp_llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model_name,
                timeout=10,
                max_tokens=600,
                max_retries=1,
                streaming=True
            )
            for chunk in temp_llm.stream(final_prompt):
                text_content = chunk.content
                if isinstance(text_content, list):
                    text_content = "".join(p.get("text", "") for p in text_content if isinstance(p, dict))
                if text_content:
                    streamed_tokens = True
                    yield str(text_content)
            if streamed_tokens:
                return
        except Exception as e:
            safe_print(f"   ⚠️ Streaming from {model_name} failed ({e}). Trying next model...")

    if not streamed_tokens:
        # Fallback to standard invoke if stream failed
        res = query_rag(user_question)
        yield res.get("answer", "")

if __name__ == "__main__":
    if not os.path.exists("./chroma_db"):
        print("Error: Vector store not found. Please run 1_build_vector_store.py first.")
    elif not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_api_key_here":
        print("Error: Missing OPENROUTER_API_KEY.")
        print("Please create a .env file, add your API key like in .env.example, and try again.")
    else:
        # Test questions
        print("Testing Political Guardrail:")
        query_rag("Who will win the upcoming presidential election?")
        
        print("\nTesting Technical ML Question:")
        query_rag("What is the Bias-Variance Tradeoff in Machine Learning?")
