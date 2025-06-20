# ===========================================
#  FastEmbed API Server - AMD64 (CPU Only)
#  docker build \
#    --platform linux/amd64 \
#    -t yaoapp/fastembed:latest-amd64 .
#
#  Build:
#  docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64 .
#
#  Usage:
#  docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-amd64
#
# ===========================================

# Build stage
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU version with explicit fallback
RUN pip install --no-cache-dir --user torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage  
FROM python:3.11-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py .
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=1
ENV ENABLE_GPU=false
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
ENTRYPOINT ["./entrypoint.sh"] 