FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-rus \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /ocr

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /ocr

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4366 --workers 4"]