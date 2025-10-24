FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY smart_retail/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY smart_retail/ ./smart_retail/
COPY artifacts/ ./artifacts/
COPY chroma_db/ ./chroma_db/

# Expose port
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health/z || exit 1

# Run the application
CMD ["python", "-m", "smart_retail.main"]
