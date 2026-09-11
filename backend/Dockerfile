FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for asyncpg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple

# Copy application code
COPY . .

# Ensure model weights and metadata are bundled for true zero-network offline capability
RUN python -c "from pathlib import Path; \
w = Path('app/ai/weights'); \
w.mkdir(parents=True, exist_ok=True); \
(w / 'model.pt').exists() or __import__('huggingface_hub').hf_hub_download(repo_id='the-harsh-vardhan/krishiclinic-crop-disease-v0-1-baseline-bmd', filename='model.pt', local_dir=str(w)); \
(w / 'metadata.json').exists() or __import__('huggingface_hub').hf_hub_download(repo_id='the-harsh-vardhan/krishiclinic-crop-disease-v0-1-baseline-bmd', filename='metadata.json', local_dir=str(w)); \
assert (w / 'model.pt').exists() and (w / 'metadata.json').exists(), 'Model weights must be bundled in app/ai/weights'"

# Create uploads directory
RUN mkdir -p uploads

# Make start script executable (handle both LF and CRLF)
COPY start.sh .
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

EXPOSE 8000

# Use start script for proper startup sequencing
ENTRYPOINT ["./start.sh"]
