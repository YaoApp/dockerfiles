# ===========================================
#  FastEmbed API Server - AMD64 with CUDA Support
#  docker build \
#    --platform linux/amd64 \
#    -t yaoapp/fastembed:latest-amd64-cuda .
#
#  Build:
#  docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64-cuda .
#
#  Usage:
#  docker run -d --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-amd64-cuda
#
# ===========================================

FROM ubuntu:22.04

# Set non-interactive installation mode to avoid timezone prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install Python 3.11 and dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    curl \
    tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Set working directory
WORKDIR /app

# Install PyTorch with CUDA support first
RUN pip3 install --no-cache-dir torch==2.1.2+cu121 --index-url https://download.pytorch.org/whl/cu121

# Copy requirements and install other Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install CUDA-specific packages
RUN pip3 install --no-cache-dir onnxruntime-gpu>=1.17.0

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
ENV ENABLE_GPU=true
ENV CUDA_VISIBLE_DEVICES=all

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
ENTRYPOINT ["./entrypoint.sh"] 