"""
Main FastAPI application for the GenAI-powered Smart Retail Experience.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

from .config import settings
from .routes import recommend_router, price_predict_router, health_router

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
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

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "GenAI-powered Smart Retail Experience API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health/"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    # Ensure directories exist
    settings.ensure_directories()
    print(f"🚀 {settings.API_TITLE} v{settings.API_VERSION} starting up...")
    print(f"📁 Artifacts directory: {settings.ARTIFACTS_DIR}")
    print(f"📁 ChromaDB directory: {settings.CHROMA_DB_DIR}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print("🛑 Application shutting down...")

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
