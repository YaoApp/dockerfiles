# FastEmbed Dockerfile

FastEmbed is a fast, lightweight, accurate library built for Retrieval Augmented Generation (RAG) and document embedding.

## Usage

### CPU Version

```bash
# AMD64
docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-amd64

# ARM64
docker run -d -p 8000:8000 -e FASTEMBED_PASSWORD=your_password yaoapp/fastembed:latest-arm64
```

### GPU Version (NVIDIA)

```bash
# AMD64 with GPU
docker run -d --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-amd64

# ARM64 with GPU
docker run -d --gpus all -p 8000:8000 -e FASTEMBED_PASSWORD=your_password -e ENABLE_GPU=true yaoapp/fastembed:latest-arm64
```

## Environment Variables

- `FASTEMBED_PASSWORD`: API authentication password (required)
- `ENABLE_GPU`: Enable GPU acceleration (optional, default: false)
- `PORT`: Server port (optional, default: 8000)
- `WORKERS`: Number of worker processes (optional, default: 1)

## Build

### AMD64

```bash
docker build --platform linux/amd64 -t yaoapp/fastembed:latest-amd64 ./amd64
```

### ARM64

```bash
docker build --platform linux/arm64 -t yaoapp/fastembed:latest-arm64 ./arm64
```

## API Endpoints

- `POST /embed` - Generate embeddings
- `GET /health` - Health check
- `GET /models` - List available models

Authentication: Add `Authorization: Bearer <FASTEMBED_PASSWORD>` header to requests.
