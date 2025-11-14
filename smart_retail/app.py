"""
Application entry point for the GenAI-powered Smart Retail Experience.

This is an alternative entry point that imports the FastAPI app
from the main module. Useful for deployment and testing.
"""

from smart_retail.main import app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    
    print(f"Starting GenAI Smart Retail API on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"ReDoc Documentation: http://{host}:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

