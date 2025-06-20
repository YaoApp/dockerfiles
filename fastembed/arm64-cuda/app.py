#!/usr/bin/env python3
"""
FastEmbed API Server with Authentication
Supports CPU and GPU acceleration
"""

import os
import logging
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
from fastembed import TextEmbedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
FASTEMBED_PASSWORD = os.environ.get("FASTEMBED_PASSWORD")
ENABLE_GPU = os.environ.get("ENABLE_GPU", "false").lower() == "true"
PORT = int(os.environ.get("PORT", 8000))
WORKERS = int(os.environ.get("WORKERS", 1))

if not FASTEMBED_PASSWORD:
    raise ValueError("FASTEMBED_PASSWORD environment variable is required")

# Global embedding model
embedding_model = None

# Security
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the API token"""
    if credentials.credentials != FASTEMBED_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup the embedding model"""
    global embedding_model
    
    # Startup
    logger.info("Initializing FastEmbed model...")
    try:
        # Initialize embedding model
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if ENABLE_GPU else ["CPUExecutionProvider"]
        embedding_model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5",
            providers=providers
        )
        logger.info(f"FastEmbed model initialized successfully (GPU: {ENABLE_GPU})")
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastEmbed service...")

# FastAPI app
app = FastAPI(
    title="FastEmbed API Server",
    description="Fast embedding service with authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Request/Response models
class EmbedRequest(BaseModel):
    texts: List[str]
    model: Optional[str] = "BAAI/bge-small-en-v1.5"

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    gpu_enabled: bool
    model_loaded: bool

class ModelsResponse(BaseModel):
    models: List[str]

# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        gpu_enabled=ENABLE_GPU,
        model_loaded=embedding_model is not None
    )

@app.get("/models", response_model=ModelsResponse, dependencies=[Depends(verify_token)])
async def list_models():
    """List available models"""
    return ModelsResponse(
        models=["BAAI/bge-small-en-v1.5"]
    )

@app.post("/embed", response_model=EmbedResponse, dependencies=[Depends(verify_token)])
async def create_embeddings(request: EmbedRequest):
    """Generate embeddings for input texts"""
    if not embedding_model:
        raise HTTPException(status_code=503, detail="Embedding model not loaded")
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    if len(request.texts) > 100:
        raise HTTPException(status_code=400, detail="Too many texts (max 100)")
    
    try:
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(request.texts)} texts")
        embeddings = list(embedding_model.embed(request.texts))
        
        return EmbedResponse(
            embeddings=[embedding.tolist() for embedding in embeddings],
            model=request.model,
            usage={
                "total_texts": len(request.texts),
                "total_tokens": sum(len(text.split()) for text in request.texts)
            }
        )
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    logger.info(f"Starting FastEmbed API server on port {PORT}")
    logger.info(f"GPU acceleration: {ENABLE_GPU}")
    logger.info(f"Workers: {WORKERS}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        workers=WORKERS,
        log_level="info"
    ) 