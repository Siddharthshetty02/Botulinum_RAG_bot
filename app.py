from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import our existing RAG querying logic
import importlib.util
spec = importlib.util.spec_from_file_location("rag", "2_query_rag.py")
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)

app = Flask(__name__)
CORS(app) # Allow Vite frontend to talk to this backend

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
        
    try:
        # Check API key before querying
        if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
            return jsonify({"answer": "Error: OPENROUTER_API_KEY is missing. Please configure your .env file."}), 500

        # Run the RAG query
        answer = rag.query_rag(question)
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error during query: {e}")
        return jsonify({"answer": f"Backend Error: {str(e)}"}), 500

# Import the upload processor
spec_upload = importlib.util.spec_from_file_location("process_upload", "3_process_upload.py")
process_upload = importlib.util.module_from_spec(spec_upload)
spec_upload.loader.exec_module(process_upload)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.lower().endswith('.pdf'):
        # Clean filename just in case
        safe_filename = "".join([c for c in file.filename if c.isalpha() or c.isdigit() or c in (' ', '.', '-', '_')]).rstrip()
        temp_pdf_path = os.path.join("data", safe_filename)
        file.save(temp_pdf_path)
        
        md_filename = safe_filename.replace('.pdf', '.md').replace('.PDF', '.md')
        
        try:
            process_upload.process_and_index_pdf(temp_pdf_path, md_filename)
            # Re-initialize the global vector_store in 2_query_rag so it sees the new data
            rag.initialize_rag_models()
            return jsonify({"message": f"Successfully indexed {safe_filename}!"})
        except Exception as e:
            print(f"Error processing upload: {e}")
            return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500
            
    return jsonify({"error": "Invalid file type. Only PDF allowed."}), 400

@app.route('/sources', methods=['GET'])
def get_sources():
    try:
        sources = process_upload.get_indexed_sources()
        return jsonify({"sources": sources})
    except Exception as e:
        print(f"Error fetching sources: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_source():
    data = request.json or {}
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "No filename provided"}), 400
        
    try:
        process_upload.delete_source_and_files(filename)
        # Re-initialize the global vector_store in 2_query_rag so it sees the updated database
        rag.initialize_rag_models()
        return jsonify({"message": f"Successfully deleted {filename} and purged vectors."})
    except Exception as e:
        print(f"Error deleting source: {e}")
        return jsonify({"error": f"Failed to delete source: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Neo UI Backend...")
    app.run(port=5000, debug=True, use_reloader=False)
