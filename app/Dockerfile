FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY main.py .
COPY templates/ ./templates/

EXPOSE 4000

ENV PRINTER_IP=192.168.50.99
ENV PRINTER_PORT=8899
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
