"""
API routes for the Smart Retail system.
"""

from .recommend import router as recommend_router
from .price_predict import router as price_predict_router
from .health import router as health_router
from .trends import router as trends_router

__all__ = ["recommend_router", "price_predict_router", "health_router", "trends_router"]
