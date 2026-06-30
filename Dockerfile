FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OCRmyPDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    ghostscript \
    libtesseract-dev \
    poppler-utils \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 5656

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5656"]
