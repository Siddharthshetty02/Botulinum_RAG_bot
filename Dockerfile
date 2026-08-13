FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for ChromaDB and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build knowledge base vector store into ChromaDB
RUN python index_kb.py

ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --timeout 120"]
