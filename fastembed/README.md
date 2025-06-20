# FastEmbed Docker Images

FastEmbed is a fast, lightweight, accurate library built for Retrieval Augmented Generation (RAG) and document embedding.

## 🏗️ Available Variants

| Variant      | Platform     | CUDA Support | Size   | Use Case                                |
| ------------ | ------------ | ------------ | ------ | --------------------------------------- |
| `amd64`      | AMD64/x86_64 | ❌ CPU Only  | ~1.2GB | General x86_64 deployment               |
| `amd64-cuda` | AMD64/x86_64 | ✅ CUDA      | ~6GB   | High-performance x86_64 with NVIDIA GPU |
| `arm64`      | ARM64        | ❌ CPU Only  | ~1.2GB | Apple Silicon, Raspberry Pi             |
| `arm64-cuda` | ARM64        | ✅ Jetson    | ~3GB   | NVIDIA Jetson devices                   |

## 🚀 Quick Build

Build all variants at once:

```bash
./build-all.sh
```

Or build individual variants:

### AMD64 CPU (Lightweight)

```bash
cd amd64
docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64 .
```

### AMD64 CUDA (CUDA Support)

```bash
cd amd64-cuda
docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64-cuda .
```

### ARM64 CPU (Lightweight)

```bash
cd arm64
docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64 .
```

### ARM64 CUDA (Jetson Support)

```bash
cd arm64-cuda
docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64-cuda .
```

## 🎯 Usage

### CPU Versions (Lightweight)

```bash
# AMD64
docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-amd64

# ARM64
docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-arm64
```

### CUDA Versions (High Performance)

```bash
# AMD64 with NVIDIA GPU
docker run -d --gpus all -p 8000:8000 \
  -e FASTEMBED_PASSWORD=your_password \
  -e ENABLE_GPU=true \
  yaoapp/fastembed:latest-amd64-cuda

# ARM64 Jetson devices
docker run -d --runtime nvidia --gpus all -p 8000:8000 \
  -e FASTEMBED_PASSWORD=your_password \
  -e ENABLE_GPU=true \
  yaoapp/fastembed:latest-arm64-cuda
```

## ⚙️ Environment Variables

- `FASTEMBED_PASSWORD`: **Required**. Authentication password for API access
- `ENABLE_GPU`: Optional. Set to `true` to enable GPU acceleration (default: `false`)
- `PORT`: Optional. Server port (default: `8000`)
- `WORKERS`: Optional. Number of worker processes (default: `1`)
- `CUDA_VISIBLE_DEVICES`: Optional. GPU device selection for multi-GPU systems

## 📡 API Endpoints

- `GET /health`: Health check endpoint (no auth required)
- `GET /models`: List available models (requires authentication)
- `POST /embed`: Generate embeddings (requires authentication)

## 🔐 Authentication

All API endpoints (except `/health`) require Bearer token authentication using the `FASTEMBED_PASSWORD` value.

Example:

```bash
curl -H "Authorization: Bearer your_password" http://localhost:8000/models
```

## 📊 Performance Comparison

| Version | Throughput       | Memory Usage | Recommended For              |
| ------- | ---------------- | ------------ | ---------------------------- |
| CPU     | ~100 texts/sec   | 1-2GB        | Development, light workloads |
| CUDA    | ~1000+ texts/sec | 4-8GB        | Production, heavy workloads  |

## 🔧 Key Differences

### CPU vs CUDA Versions

**CPU Versions (`amd64`, `arm64`)**:

- Small image size (~1.2GB)
- Lower memory usage
- No special hardware requirements
- Good for development and light workloads

**CUDA Versions (`amd64-cuda`, `arm64-cuda`)**:

- Larger image size (3-6GB)
- Higher memory usage
- Requires NVIDIA GPU and Docker GPU support
- Significant performance improvement for batch processing
