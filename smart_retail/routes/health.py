"""
Health check endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, Depends
from ..models.data_models import HealthResponse
from ..models.ml_models import ModelManager

router = APIRouter(prefix="/health", tags=["health"])

# Global model manager instance
model_manager = ModelManager()

@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="""
    Comprehensive health check endpoint to verify model and database status.
    
    This endpoint provides detailed information about:
    - API status
    - Model availability (fast models, original model, fallback model)
    - Recommendation system status (ChromaDB, embedding model)
    - Number of items in the recommendation index
    - Currently active model type
    
    **Example Response:**
    ```json
    {
        "status": "ok",
        "fast_models_loaded": true,
        "original_model_loaded": true,
        "recs_index_loaded": true,
        "recs_count": 1500,
        "embedding_model_loaded": true,
        "model_type_in_use": "fast_multi_model",
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    responses={
        200: {
            "description": "Health status of the API",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "fast_models_loaded": True,
                        "original_model_loaded": True,
                        "recs_index_loaded": True,
                        "recs_count": 1500,
                        "embedding_model_loaded": True,
                        "model_type_in_use": "fast_multi_model",
                        "timestamp": "2024-01-15T10:30:00"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Health check endpoint to verify model and database status.
    
    Returns:
        HealthResponse: Status of all system components
    """
    health_status = model_manager.get_health_status()
    
    return HealthResponse(
        status="ok",
        **health_status
    )

@router.get(
    "/z",
    summary="Simple Health Check",
    description="""
    Simple health check endpoint (alternative to /health/).
    
    This is a lightweight health check endpoint that returns basic
    health status. Useful for load balancers and monitoring systems.
    
    **Example Response:**
    ```json
    {
        "status": "ok",
        "fast_models_loaded": true,
        "original_model_loaded": true,
        "recs_index_loaded": true,
        "recs_count": 1500,
        "embedding_model_loaded": true,
        "model_type_in_use": "fast_multi_model"
    }
    ```
    """,
    responses={
        200: {
            "description": "Basic health status",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "fast_models_loaded": True,
                        "original_model_loaded": True,
                        "recs_index_loaded": True,
                        "recs_count": 1500,
                        "embedding_model_loaded": True,
                        "model_type_in_use": "fast_multi_model"
                    }
                }
            }
        }
    }
)
async def healthz():
    """
    Simple health check endpoint (alternative to /health/).
    
    Returns:
        dict: Basic health status
    """
    health_status = model_manager.get_health_status()
    
    return {
        "status": "ok",
        **health_status
    }
