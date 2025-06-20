# ===========================================
#  FastEmbed API Server - ARM64 with CUDA Support (Jetson)
#  docker build \
#    --platform linux/arm64 \
#    -t yaoapp/fastembed:latest-arm64-cuda .
#
#  Build:
#  docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64-cuda .
#
#  Usage:
#  docker run -d --runtime nvidia --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-arm64-cuda
#
#  Note: This is designed for NVIDIA Jetson devices
#
# ===========================================

FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
COPY requirements-gpu-arm64.txt .
RUN pip3 install --no-cache-dir -r requirements-gpu-arm64.txt

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

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
ENTRYPOINT ["./entrypoint.sh"] 