from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os
import json
import uuid
from datetime import datetime
import importlib.util

# Import RAG module
spec = importlib.util.spec_from_file_location("rag", "2_query_rag.py")
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)

# Import RL engine
spec_rl = importlib.util.spec_from_file_location("rl_engine", "rl_feedback_engine.py")
rl_engine = importlib.util.module_from_spec(spec_rl)
spec_rl.loader.exec_module(rl_engine)

# Import upload processor
spec_upload = importlib.util.spec_from_file_location("process_upload", "3_process_upload.py")
process_upload = importlib.util.module_from_spec(spec_upload)
spec_upload.loader.exec_module(process_upload)

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from frontend UI

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Botulinum RAG Studio Backend is running!"})

LOGS_FILE = "chat_logs.jsonl"
FEEDBACK_FILE = "feedback_logs.jsonl"

def log_interaction(log_data):
    try:
        with open(LOGS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

def log_feedback(feedback_data):
    try:
        with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_data) + "\n")
    except Exception as e:
        print(f"Failed to write feedback: {e}")

@app.route('/chat_stream', methods=['POST'])
def chat_stream():
    data = request.json or {}
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
        
    log_id = str(uuid.uuid4())
    
    def generate():
        full_tokens = []
        try:
            for token in rag.query_rag_stream(question):
                full_tokens.append(token)
                payload = json.dumps({"token": token, "log_id": log_id})
                yield f"data: {payload}\n\n"
            
            # Log complete interaction once stream finishes
            log_interaction({
                "id": log_id,
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": "".join(full_tokens)
            })
            yield f"data: {json.dumps({'done': True, 'log_id': log_id})}\n\n"
        except Exception as e:
            print(f"Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
        
    try:
        if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
            return jsonify({"answer": "Error: OPENROUTER_API_KEY is missing. Please configure your .env file."}), 500

        res = rag.query_rag(question)
        if isinstance(res, dict):
            answer = res.get("answer", "")
            is_fast_path = res.get("is_fast_path", False)
        else:
            answer = str(res)
            is_fast_path = False

        log_id = str(uuid.uuid4())
        
        log_interaction({
            "id": log_id,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "is_fast_path": is_fast_path
        })
        
        return jsonify({"answer": answer, "log_id": log_id, "is_fast_path": is_fast_path})
    except Exception as e:
        print(f"Error during query: {e}")
        return jsonify({"answer": f"Backend Error: {str(e)}"}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json or {}
    log_id = data.get('log_id')
    rating = data.get('rating') # 'up' or 'down'
    comment = data.get('comment', '')
    
    if not log_id or not rating:
        return jsonify({"error": "Missing log_id or rating"}), 400
        
    log_feedback({
        "log_id": log_id,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().isoformat()
    })
    
    try:
        rl_stats = rl_engine.optimize_rl_rewards()
        return jsonify({"message": "Feedback recorded & RL rewards updated!", "rl_stats": rl_stats})
    except Exception as e:
        print(f"RL Optimization error: {e}")
        return jsonify({"message": "Feedback recorded successfully!"})

@app.route('/rl_status', methods=['GET'])
def get_rl_status():
    try:
        rl_state = rl_engine.load_rl_rewards()
        return jsonify(rl_state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.lower().endswith('.pdf'):
        safe_filename = "".join([c for c in file.filename if c.isalpha() or c.isdigit() or c in (' ', '.', '-', '_')]).rstrip()
        temp_pdf_path = os.path.join("data", safe_filename)
        file.save(temp_pdf_path)
        
        md_filename = safe_filename.replace('.pdf', '.md').replace('.PDF', '.md')
        
        try:
            process_upload.process_and_index_pdf(temp_pdf_path, md_filename)
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
        rag.initialize_rag_models()
        return jsonify({"message": f"Successfully deleted {filename} and purged vectors."})
    except Exception as e:
        print(f"Error deleting source: {e}")
        return jsonify({"error": f"Failed to delete source: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Neo UI Backend with Word-by-Word Streaming...")
    app.run(port=5000, debug=True, use_reloader=False)
