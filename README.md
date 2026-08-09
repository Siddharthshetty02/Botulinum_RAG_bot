# ⚡ Botulinum Bot - Neural RAG Studio

**Botulinum Bot** is a modern, high-performance Retrieval-Augmented Generation (RAG) studio powered by **OpenRouter's free open-weight LLMs** (`openai/gpt-oss-20b:free`), local **ChromaDB** vector storage, and an **HTML5 5-Layer Artificial Neural Network Visualizer**.

---

## ✨ Features

- 🧠 **Open-Weight RAG Architecture**: Integrated with `openai/gpt-oss-20b:free` via OpenRouter for low-latency contextual inference.
- 📄 **Smart PDF-to-Markdown Conversion**: Uses `pymupdf4llm` to transform uploaded PDF documents into structured `.md` files prior to text chunking and vector indexing.
- ⚡ **Local Vector Store**: Built with **ChromaDB** and `sentence-transformers/all-MiniLM-L6-v2` embeddings for fast semantic retrieval.
- 🔮 **5-Layer Artificial Neural Network Visualizer**: Interactive Glassmorphism pop-up overlay canvas rendering real-time forward propagation pulses during vector search.
- 🗑️ **Source Storage Reclamation**: Delete documents from disk and purge vector embeddings from ChromaDB directly from the Knowledge Base sidebar.
- 🎨 **Sleek OpenRouter Dark Theme**: Modern Tailwind CSS interface with responsive 2-column layout.

---

## 🛠️ Architecture

```
[ User Input / PDF Upload ]
           │
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
           ├── (Animated via 5-Layer ANN Visualizer)
           ▼
[ OpenRouter LLM API (gpt-oss-20b:free) ] ──► [ User Response ]
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

1. **Build Initial Vector Index** (Optional if sample data exists):
   ```bash
   python 1_build_vector_store.py
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

4. **Access Botulinum Bot**:
   Open your browser and navigate to `http://localhost:3000`.

---

## 📁 Project Structure

```
Botulinum_RAG_bot/
├── 1_build_vector_store.py   # Script to process data/ files & populate ChromaDB
├── 2_query_rag.py            # Core RAG retrieval & OpenRouter inference pipeline
├── 3_process_upload.py       # PDF to Markdown parser & Chroma deletion engine
├── app.py                    # Flask REST API endpoints (/chat, /upload, /sources, /delete)
├── requirements.txt          # Python dependencies
├── .env                      # API environment variables (OpenRouter API key)
├── data/                     # Source documents directory (.pdf, .md, .txt)
├── chroma_db/                # Local persistent Chroma vector database
└── neo-ui/                   # Frontend Studio application
    ├── index.html            # Studio workspace with ANN overlay visualizer
    ├── style.css             # Glassmorphism & pulse animation styles
    └── main.js               # Canvas 5-layer ANN visualizer & API integration
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
