---
title: Botulinum Rag Backend
emoji: 🧪
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
---

# ⚡ Botulinum Bot - Machine Learning RAG Studio

**Botulinum Bot** is a high-performance Retrieval-Augmented Generation (RAG) studio fine-tuned for **Machine Learning (ML)** engineering. Powered by **OpenRouter's free open-weight LLMs** (`openai/gpt-oss-20b:free`), local **ChromaDB** vector storage, **RL feedback keyword re-ranking**, **DPO preference dataset generation**, and strict **Safety Guardrails**.

---

## ✨ Features & Component Rationale

- 🎯 **Fine-Tuned ML Specialist Persona**: System instructions calibrated specifically for technical Machine Learning concepts (Supervised/Unsupervised Learning, XGBoost, Cross-Validation, Bias-Variance, Evaluation Metrics).
- 🛡️ **Political & Domain Guardrail Engine**: Fast-path regex classifier and safety prompt directives preventing off-topic, election, or political queries.
- 🧠 **Open-Weight RAG Architecture**: Integrated with `openai/gpt-oss-20b:free` via OpenRouter for low-latency contextual inference.
- 📄 **Smart PDF-to-Markdown Conversion**: Uses `pymupdf4llm` to transform uploaded PDF documents into structured `.md` files prior to text chunking and vector indexing.
- ⚡ **Local Vector Store & RL Re-ranking**: Built with **ChromaDB** and `sentence-transformers/all-MiniLM-L6-v2` embeddings, boosted with RL reward weights for key ML concepts.
- ⚙️ **ML Fine-Tuning Pipeline (`4_fine_tune_ml.py`)**: Script to optimize vector indices, RL keyword reward weights (`rl_rewards.json`), and export DPO preference pairs (`dpo_dataset.json`).
- 🗑️ **Source Storage Reclamation**: Delete documents from disk and purge vector embeddings from ChromaDB directly from the Knowledge Base sidebar.
- 🎨 **Clean ML Studio Interface**: Modern dark-themed responsive studio UI built with Tailwind CSS.

---

## 💡 Why We Built & Added Each Component

### 1. Fine-Tuning for Machine Learning (ML)
- **Why it was built**: Generic LLMs often produce vague, superficial text when asked about complex data science algorithms. We fine-tuned the prompt template, retrieval scoring weights, and candidate re-ranking specifically for **Machine Learning (ML)**.
- **Benefits**: Ensures responses include mathematical intuition, exact algorithm mechanics (e.g. XGBoost split finding, loss regularization), code snippets in Python/Scikit-Learn, and structured hyperparameter recommendations.

### 2. Political Guardrail Engine (`check_political_guardrail`)
- **Why it was built**: RAG engines deployed in technical environments must stay strictly within domain scope and avoid serving non-technical, partisan, or controversial political opinions.
- **Benefits**: Intercepts political, election, and partisan queries at the fast-path layer instantly (0ms latency, zero API cost) and returns a polite redirect guiding users back to technical ML and document queries.

### 3. Removal of Neural Network Animation Canvas Visualizer
- **Why it was removed**: The 5-layer Artificial Neural Network canvas visualizer added background CPU/GPU overhead and distracted from the core functional workspace.
- **Benefits**: Dramatically improves frontend UI render performance, reduces DOM footprint, and presents a sleek, high-density professional developer studio.

### 4. Reinforcement Learning (RL) Keyword Re-Ranking (`rl_feedback_engine.py`)
- **Why it was built**: Pure vector similarity (cosine distance) can sometimes retrieve irrelevant context chunks if phrasing varies. By tracking user feedback (👍/👎), the system calculates Temporal Difference (TD) Q-learning reward weights $R \in [+1.0, -1.0]$ for key domain terms.
- **Benefits**: Dynamically boosts high-performing ML context chunks during vector search, improving retrieval precision over time based on real user interactions.

### 5. DPO Preference Dataset Generator (`dpo_dataset.json`)
- **Why it was built**: Fine-tuning local LLMs via Direct Preference Optimization (DPO) requires high-quality `{prompt, chosen, rejected}` dataset triples.
- **Benefits**: Automatically converts positive and negative user feedback logs into a standardized DPO dataset ready for downstream model fine-tuning and alignment.

### 6. Smart PDF-to-Markdown Ingestion (`3_process_upload.py`)
- **Why it was built**: Raw PDF text extractors strip headings, tables, bullet points, and code formatting, degrading RAG embedding quality.
- **Benefits**: Uses `pymupdf4llm` to preserve markdown syntax (headers `#`, lists, tables) before splitting with `MarkdownTextSplitter`, ensuring vector chunks retain semantic document hierarchy.

---

## 🛠️ Architecture

```
[ User Input / PDF Upload ]
           │
           ├── (0. Fast-Path Political Guardrail & Creator Check)
           ▼
[ PyMuPDF Markdown Parser ] ──► Stores (.md) in data/
           │
           ▼
[ MarkdownTextSplitter ]
           │
           ▼
[ MiniLM Embeddings Engine ]
           │
           ▼
[ ChromaDB Vector Store ]
           │
           ├── (1. RL Keyword Re-ranking & ML Domain Weighting)
           ▼
[ OpenRouter LLM API (gpt-oss-20b:free) ] ──► [ Fine-Tuned ML Response ]
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An OpenRouter API Key ([Get a free key here](https://openrouter.ai/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Siddharthshetty02/Botulinum_RAG_bot.git
   cd Botulinum_RAG_bot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

---

## 🏃 Running the Application

1. **Build Initial Vector Index & Fine-Tune for ML**:
   ```bash
   python 4_fine_tune_ml.py
   ```

2. **Start Python Backend Server**:
   ```bash
   python app.py
   ```
   *The backend REST API runs on `http://localhost:5000`.*

3. **Start Frontend Web UI**:
   Open a separate terminal window:
   ```bash
   python -m http.server 3000 --directory neo-ui
   ```

4. **Access Botulinum Bot Studio**:
   Open your browser and navigate to `http://localhost:3000`.

---

## 📁 Project Structure & Module Descriptions

```
Botulinum_RAG_bot/
├── 1_build_vector_store.py   # Script to process sample document into ChromaDB
├── 2_query_rag.py            # Fine-tuned ML RAG retrieval, guardrails & OpenRouter inference engine
├── 3_process_upload.py       # PDF to Markdown parser & Chroma deletion engine
├── 4_fine_tune_ml.py         # Fine-tuning runner for ML vector indexing & RL rewards
├── app.py                    # Flask REST API endpoints (/chat, /upload, /sources, /delete, /feedback)
├── rl_feedback_engine.py     # Reinforcement Learning feedback & DPO pair generator
├── rl_rewards.json           # Saved ML topic reward weights
├── dpo_dataset.json          # Exported DPO preference pairs for LLM fine-tuning
├── requirements.txt          # Python dependencies
├── .env                      # API environment variables (OpenRouter API key)
├── data/                     # Source documents directory (.pdf, .md, .txt)
├── chroma_db/                # Local persistent Chroma vector database
└── neo-ui/                   # Frontend Studio application workspace
    ├── index.html            # Clean ML Studio UI
    ├── style.css             # Dark mode styles & custom scrollbars
    └── main.js               # Chat & Knowledge Base API integration
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
