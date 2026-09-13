FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (ffmpeg for stream recording)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Prepare recordings storage
RUN mkdir -p /app/recordings

# Copy application source
COPY main.py .
COPY templates/ ./templates/

EXPOSE 4000

ENV PRINTER_IP=192.168.50.99
ENV PRINTER_PORT=8899
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
