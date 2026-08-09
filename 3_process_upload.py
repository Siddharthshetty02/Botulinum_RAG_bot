import os
import pymupdf4llm
import fitz # PyMuPDF fallback
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))

def process_and_index_pdf(pdf_path, output_md_name):
    """
    Takes a PDF, converts it to Markdown using pymupdf4llm (with PyMuPDF fallback),
    saves the Markdown, and indexes it into the Chroma DB.
    """
    safe_print(f"1. Converting {pdf_path} to Markdown...")
    try:
        # Convert PDF to Markdown string
        md_text = pymupdf4llm.to_markdown(pdf_path)
    except Exception as e:
        safe_print(f"pymupdf4llm conversion failed ({e}), using PyMuPDF text fallback...")
        doc = fitz.open(pdf_path)
        md_text = ""
        for i, page in enumerate(doc):
            md_text += f"# Page {i+1}\n\n" + page.get_text() + "\n\n"
        doc.close()
    
    # Save the markdown to a file
    md_file_path = os.path.join("data", output_md_name)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    safe_print(f"   Saved markdown to {md_file_path}")
    
    safe_print("2. Splitting Markdown into chunks...")
    loader = TextLoader(md_file_path, encoding="utf-8")
    documents = loader.load()
    
    # MarkdownTextSplitter is smart about headers and structure
    text_splitter = MarkdownTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    safe_print(f"   Created {len(chunks)} chunks.")
    
    safe_print("3. Loading existing Vector Store...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    safe_print("4. Adding new documents to Vector Store...")
    vector_store.add_documents(chunks)
    
    safe_print(f"Successfully indexed {pdf_path} into the vector store!")
    return True

def delete_source_and_files(filename):
    """
    Deletes the pdf, md, or txt file matching filename from data/
    and deletes its embedded vectors from Chroma DB.
    """
    base_name = os.path.splitext(filename)[0]
    
    # Identify files associated with this base name
    possible_files = [
        os.path.join("data", f"{base_name}.pdf"),
        os.path.join("data", f"{base_name}.md"),
        os.path.join("data", f"{base_name}.txt"),
        os.path.join("data", filename)
    ]
    
    deleted_files = []
    for filepath in set(possible_files):
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                deleted_files.append(filepath)
                safe_print(f"Removed file from disk: {filepath}")
            except Exception as e:
                safe_print(f"Error removing {filepath}: {e}")
                
    # Remove vector embeddings from Chroma
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        
        # Check source paths
        sources_to_check = [
            os.path.join("data", f"{base_name}.md"),
            os.path.join("data", f"{base_name}.txt"),
            os.path.join("data", f"{base_name}.pdf")
        ]
        
        for s in sources_to_check:
            # Check both forward and backward slashes for Windows compatibility
            for path_variant in [s, s.replace("/", "\\"), s.replace("\\", "/")]:
                matching = vector_store.get(where={"source": path_variant})
                if matching and matching.get("ids"):
                    vector_store.delete(ids=matching["ids"])
                    safe_print(f"Deleted {len(matching['ids'])} vectors matching {path_variant} from Chroma DB.")
    except Exception as e:
        safe_print(f"Error purging vectors from Chroma: {e}")
        
    return True

def get_indexed_sources():
    """
    Returns list of files currently in data/ directory.
    """
    sources = []
    if os.path.exists("data"):
        files = os.listdir("data")
        grouped = {}
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.pdf', '.md', '.txt'):
                base = os.path.splitext(f)[0]
                full_path = os.path.join("data", f)
                size_kb = round(os.path.getsize(full_path) / 1024, 1)
                
                if base not in grouped:
                    grouped[base] = {
                        "name": base,
                        "files": [],
                        "total_kb": 0.0
                    }
                grouped[base]["files"].append(f)
                grouped[base]["total_kb"] += size_kb
                
        for base, info in grouped.items():
            sources.append({
                "name": base,
                "files": info["files"],
                "size_kb": round(info["total_kb"], 1)
            })
    return sources

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python 3_process_upload.py <pdf_path> <output_md_name>")
    else:
        process_and_index_pdf(sys.argv[1], sys.argv[2])
