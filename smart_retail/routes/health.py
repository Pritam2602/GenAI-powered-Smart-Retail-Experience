"""
Health check endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, Depends
from ..models.data_models import HealthResponse
from ..models.ml_models import ModelManager

router = APIRouter(prefix="/health", tags=["health"])

# Global model manager instance
model_manager = ModelManager()

@router.get("/", response_model=HealthResponse)
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

@router.get("/z")
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
