# Regulatory Capital & Fairness Agentic RAG System
# Multi-stage Docker build for production deployment

# ========================================
# Stage 1: Builder
# ========================================
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    pip install --no-cache-dir -e .

# ========================================
# Stage 2: Runtime
# ========================================
FROM python:3.11-slim

LABEL maintainer="vadagaVenkatesh"
LABEL description="Agentic RAG System for Regulatory Compliance"
LABEL version="0.1.0"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 raguser && \
    chown -R raguser:raguser /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=raguser:raguser app/ /app/app/
COPY --chown=raguser:raguser config/ /app/config/
COPY --chown=raguser:raguser examples/ /app/examples/
COPY --chown=raguser:raguser pyproject.toml /app/

# Create data directory
RUN mkdir -p /app/data /app/data/chroma /app/data/faiss_indices && \
    chown -R raguser:raguser /app/data

# Switch to non-root user
USER raguser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
