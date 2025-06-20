#!/bin/bash

# FastEmbed Docker Image Build Script
# Builds all versions: CPU and CUDA variants for both AMD64 and ARM64

set -e

echo "🚀 Building FastEmbed Docker Images..."

# Build AMD64 CPU version (lightweight)
echo "📦 Building AMD64 CPU version..."
docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64 ./amd64/

# Build AMD64 CUDA version (with CUDA support)
echo "🔥 Building AMD64 CUDA version..."
docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64-cuda ./amd64-cuda/

# Build ARM64 CPU version (lightweight)
echo "📦 Building ARM64 CPU version..."
docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64 ./arm64/

# Build ARM64 CUDA version (for Jetson devices)
echo "🔥 Building ARM64 CUDA version (Jetson)..."
docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64-cuda ./arm64-cuda/

echo "✅ All builds completed!"

echo ""
echo "📋 Built Images:"
echo "  • yaoapp/fastembed:latest-amd64       - AMD64 CPU (~1.2GB)"
echo "  • yaoapp/fastembed:latest-amd64-cuda  - AMD64 CUDA (~6GB)"
echo "  • yaoapp/fastembed:latest-arm64       - ARM64 CPU (~1.2GB)"
echo "  • yaoapp/fastembed:latest-arm64-cuda  - ARM64 CUDA for Jetson (~3GB)"

echo ""
echo "🚀 Usage Examples:"
echo "  # CPU versions:"
echo "  docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-amd64"
echo "  docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-arm64"
echo ""
echo "  # CUDA versions:"
echo "  docker run -d --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-amd64-cuda"
echo "  docker run -d --runtime nvidia --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-arm64-cuda" 