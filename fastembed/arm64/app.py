#!/usr/bin/env python3
"""
FastEmbed API Server with Authentication
Supports CPU and GPU acceleration with dynamic model loading
Supports both dense and sparse text embedding models
"""

import os
import logging
from typing import List, Optional, Dict, Any, Union
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
from fastembed import TextEmbedding, SparseTextEmbedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
FASTEMBED_PASSWORD = os.environ.get("FASTEMBED_PASSWORD")
ENABLE_GPU = os.environ.get("ENABLE_GPU", "false").lower() == "true"
PORT = int(os.environ.get("PORT", 8000))
WORKERS = int(os.environ.get("WORKERS", 1))
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "BAAI/bge-small-en-v1.5")
MAX_TEXTS_PER_REQUEST = int(os.environ.get("MAX_TEXTS_PER_REQUEST", 2000))

if not FASTEMBED_PASSWORD:
    raise ValueError("FASTEMBED_PASSWORD environment variable is required")

# Global model cache for both dense and sparse models
dense_model_cache: Dict[str, TextEmbedding] = {}
sparse_model_cache: Dict[str, SparseTextEmbedding] = {}

# Supported dense models from FastEmbed documentation
SUPPORTED_DENSE_MODELS = [
    "BAAI/bge-small-en-v1.5",
    "BAAI/bge-small-zh-v1.5", 
    "snowflake/snowflake-arctic-embed-xs",
    "sentence-transformers/all-MiniLM-L6-v2",
    "jinaai/jina-embeddings-v2-small-en",
    "BAAI/bge-small-en",
    "snowflake/snowflake-arctic-embed-s",
    "nomic-ai/nomic-embed-text-v1.5-Q",
    "BAAI/bge-base-en-v1.5",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "Qdrant/clip-ViT-B-32-text",
    "jinaai/jina-embeddings-v2-base-de",
    "BAAI/bge-base-en",
    "snowflake/snowflake-arctic-embed-m",
    "nomic-ai/nomic-embed-text-v1.5",
    "jinaai/jina-embeddings-v2-base-en",
    "nomic-ai/nomic-embed-text-v1",
    "snowflake/snowflake-arctic-embed-m-long",
    "mixedbread-ai/mxbai-embed-large-v1",
    "jinaai/jina-embeddings-v2-base-code",
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    "snowflake/snowflake-arctic-embed-l",
    "thenlper/gte-large",
    "BAAI/bge-large-en-v1.5",
    "intfloat/multilingual-e5-large"
]

# Supported sparse models from FastEmbed documentation
SUPPORTED_SPARSE_MODELS = [
    "Qdrant/bm25",
    "Qdrant/bm42-all-minilm-l6-v2-attentions",
    "prithivida/Splade_PP_en_v1",
    "prithvida/Splade_PP_en_v1"
]

# All supported models
SUPPORTED_MODELS = SUPPORTED_DENSE_MODELS + SUPPORTED_SPARSE_MODELS

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

def is_sparse_model(model_name: str) -> bool:
    """Check if the model is a sparse embedding model"""
    return model_name in SUPPORTED_SPARSE_MODELS

def get_or_load_dense_model(model_name: str) -> TextEmbedding:
    """Get dense model from cache or load it"""
    if model_name not in dense_model_cache:
        logger.info(f"Loading dense model: {model_name}")
        try:
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if ENABLE_GPU else ["CPUExecutionProvider"]
            dense_model_cache[model_name] = TextEmbedding(
                model_name=model_name,
                providers=providers
            )
            logger.info(f"Dense model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load dense model {model_name}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load dense model {model_name}: {str(e)}"
            )
    
    return dense_model_cache[model_name]

def get_or_load_sparse_model(model_name: str) -> SparseTextEmbedding:
    """Get sparse model from cache or load it"""
    if model_name not in sparse_model_cache:
        logger.info(f"Loading sparse model: {model_name}")
        try:
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if ENABLE_GPU else ["CPUExecutionProvider"]
            sparse_model_cache[model_name] = SparseTextEmbedding(
                model_name=model_name,
                providers=providers
            )
            logger.info(f"Sparse model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sparse model {model_name}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load sparse model {model_name}: {str(e)}"
            )
    
    return sparse_model_cache[model_name]

def get_or_load_model(model_name: str) -> Union[TextEmbedding, SparseTextEmbedding]:
    """Get model from cache or load it (handles both dense and sparse models)"""
    if model_name not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=400, 
            detail=f"Model '{model_name}' is not supported. Use /models endpoint to see supported models."
        )
    
    if is_sparse_model(model_name):
        return get_or_load_sparse_model(model_name)
    else:
        return get_or_load_dense_model(model_name)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup"""
    
    # Startup - preload default model
    logger.info("Initializing FastEmbed service...")
    try:
        logger.info(f"Preloading default model: {DEFAULT_MODEL}")
        get_or_load_model(DEFAULT_MODEL)
        logger.info(f"FastEmbed service initialized successfully (GPU: {ENABLE_GPU})")
    except Exception as e:
        logger.error(f"Failed to initialize default model: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastEmbed service...")
    dense_model_cache.clear()
    sparse_model_cache.clear()

# FastAPI app
app = FastAPI(
    title="FastEmbed API Server",
    description="Fast embedding service with authentication and multiple model support (dense and sparse)",
    version="2.1.0",
    lifespan=lifespan
)

# Request/Response models
class EmbedRequest(BaseModel):
    texts: List[str]
    model: Optional[str] = DEFAULT_MODEL

class DenseEmbedResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, Any]

class SparseEmbedding(BaseModel):
    indices: List[int]
    values: List[float]

class SparseEmbedResponse(BaseModel):
    embeddings: List[SparseEmbedding]
    model: str
    usage: Dict[str, Any]

# Union type for both response types
EmbedResponse = Union[DenseEmbedResponse, SparseEmbedResponse]

class HealthResponse(BaseModel):
    status: str
    gpu_enabled: bool
    loaded_dense_models: List[str]
    loaded_sparse_models: List[str]
    supported_models_count: int

class ModelsResponse(BaseModel):
    dense_models: List[str]
    sparse_models: List[str]
    all_models: List[str]
    loaded_dense_models: List[str]
    loaded_sparse_models: List[str]
    default_model: str

# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        gpu_enabled=ENABLE_GPU,
        loaded_dense_models=list(dense_model_cache.keys()),
        loaded_sparse_models=list(sparse_model_cache.keys()),
        supported_models_count=len(SUPPORTED_MODELS)
    )

@app.get("/models", response_model=ModelsResponse, dependencies=[Depends(verify_token)])
async def list_models():
    """List available and loaded models"""
    return ModelsResponse(
        dense_models=SUPPORTED_DENSE_MODELS,
        sparse_models=SUPPORTED_SPARSE_MODELS,
        all_models=SUPPORTED_MODELS,
        loaded_dense_models=list(dense_model_cache.keys()),
        loaded_sparse_models=list(sparse_model_cache.keys()),
        default_model=DEFAULT_MODEL
    )

@app.post("/embed", dependencies=[Depends(verify_token)])
async def create_embeddings(request: EmbedRequest):
    """Generate embeddings for input texts (supports both dense and sparse models)"""
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    if len(request.texts) > MAX_TEXTS_PER_REQUEST:
        raise HTTPException(status_code=400, detail=f"Too many texts (max {MAX_TEXTS_PER_REQUEST})")
    
    try:
        # Get or load the requested model
        model = get_or_load_model(request.model)
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(request.texts)} texts using model: {request.model}")
        
        if is_sparse_model(request.model):
            # Handle sparse embeddings
            embeddings = list(model.embed(request.texts))
            
            # Convert sparse embeddings to the expected format
            sparse_embeddings = []
            for embedding in embeddings:
                # embedding is a scipy sparse matrix
                coo_matrix = embedding.tocoo()
                sparse_embeddings.append(SparseEmbedding(
                    indices=coo_matrix.col.tolist(),
                    values=coo_matrix.data.tolist()
                ))
            
            return SparseEmbedResponse(
                embeddings=sparse_embeddings,
                model=request.model,
                usage={
                    "total_texts": len(request.texts),
                    "total_tokens": sum(len(text.split()) for text in request.texts),
                    "embedding_type": "sparse"
                }
            )
        else:
            # Handle dense embeddings
            embeddings = list(model.embed(request.texts))
            
            return DenseEmbedResponse(
                embeddings=[embedding.tolist() for embedding in embeddings],
                model=request.model,
                usage={
                    "total_texts": len(request.texts),
                    "total_tokens": sum(len(text.split()) for text in request.texts),
                    "embedding_type": "dense"
                }
            )
    except HTTPException:
        raise
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
    logger.info(f"Default model: {DEFAULT_MODEL}")
    logger.info(f"Supported dense models: {len(SUPPORTED_DENSE_MODELS)}")
    logger.info(f"Supported sparse models: {len(SUPPORTED_SPARSE_MODELS)}")
    logger.info(f"Total supported models: {len(SUPPORTED_MODELS)}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        workers=WORKERS,
        log_level="info"
    ) 