"""
Main FastAPI application for the GenAI-powered Smart Retail Experience.

This is a professional, production-ready API for fashion product recommendations
and price prediction using AI/ML models.

Features:
- AI-powered price prediction with specialized models for different product types
- Vector-based product recommendations using sentence transformers
- Comprehensive API documentation with examples
- Input validation and error handling
- Health check endpoints for monitoring
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import uvicorn
import os
import logging
from typing import Dict

from .config import settings
from .routes import recommend_router, price_predict_router, health_router, trends_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    ## GenAI-powered Smart Retail Experience API
    
    A professional AI-powered fashion recommendation and price prediction system.
    
    ### Features
    
    * **AI Price Prediction**: Multi-model system with specialized models for different product types
      - Jewelry Model: Gold, silver, diamonds, precious stones
      - Watch Model: Timepieces, movements, luxury brands
      - Luxury Apparel Model: Designer, premium, high-end fashion
      - Standard Apparel Model: Regular clothing and accessories
    
    * **Smart Recommendations**: Vector-based product recommendations using sentence transformers
      - Semantic search using ChromaDB
      - Cosine similarity for finding similar products
      - Configurable number of results
    
    * **Health Monitoring**: Comprehensive health check endpoints
      - Model status monitoring
      - Database connectivity checks
      - Service availability status
    
    * **Fashion Trend Analysis**: Advanced trend analysis endpoints
      - Trending colors and styles
      - Seasonal trends
      - Price trends
      - Sustainability trends
      - Brand performance analysis
    
    * **Explainable AI**: Price prediction explainability
      - Feature importance analysis
      - Key factors identification
      - Price breakdown
      - Recommendations
    
    ### API Documentation
    
    * **Interactive Docs**: Visit `/docs` for Swagger UI
    * **ReDoc**: Visit `/redoc` for alternative documentation
    
    ### Getting Started
    
    1. Check API health: `GET /health/`
    2. Predict price: `POST /predict/price` (add `?explain=true` for explanation)
    3. Get recommendations: `POST /recommend/products`
    4. Get trends: `GET /trends/colors`, `GET /trends/styles`, `GET /trends/seasonal`
    5. Analyze brands: `POST /trends/brands`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
    servers=[
        {
            "url": "http://localhost:8001",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include routers
app.include_router(health_router)
app.include_router(price_predict_router)
app.include_router(recommend_router)
app.include_router(trends_router)

# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Get API information and available endpoints",
    response_description="API information and links to documentation"
)
async def root() -> Dict[str, str]:
    """
    Root endpoint with API information.
    
    Returns:
        Dictionary containing API information, version, and links to documentation
    """
    return {
        "message": "GenAI-powered Smart Retail Experience API",
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health/",
        "endpoints": {
            "health": "/health/",
            "predict_price": "/predict/price",
            "recommend_products": "/recommend/products",
            "trends": "/trends/",
            "trending_colors": "/trends/colors",
            "trending_styles": "/trends/styles",
            "seasonal_trends": "/trends/seasonal",
            "price_trends": "/trends/price",
            "sustainability_trends": "/trends/sustainability",
            "trend_report": "/trends/report",
            "brand_analysis": "/trends/brands"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The request that caused the error
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__,
            "path": str(request.url)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    
    This function is called when the application starts up.
    It ensures all required directories exist and logs startup information.
    """
    # Ensure directories exist
    settings.ensure_directories()
    logger.info(f" {settings.API_TITLE} v{settings.API_VERSION} starting up...")
    logger.info(f" Artifacts directory: {settings.ARTIFACTS_DIR}")
    logger.info(f" ChromaDB directory: {settings.CHROMA_DB_DIR}")
    logger.info(" Application startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown.
    
    This function is called when the application shuts down.
    Perform any necessary cleanup tasks here.
    """
    logger.info(" Application shutting down...")
    logger.info(" Application shutdown complete")

if __name__ == "__main__":
    # Get port from environment variable or default to 8001
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "smart_retail.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
