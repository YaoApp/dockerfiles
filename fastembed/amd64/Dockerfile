# ===========================================
#  FastEmbed API Server - AMD64
#  docker build \
#    --platform linux/amd64 \
#    -t yaoapp/fastembed:latest-amd64 .
#
#  Build:
#  docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64 .
#
#  Usage:
#  docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-amd64
#  docker run -d --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-amd64
#
# ===========================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install NVIDIA CUDA toolkit for GPU support (optional)
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && apt-get update \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
ENTRYPOINT ["./entrypoint.sh"] 