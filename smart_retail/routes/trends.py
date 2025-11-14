"""
Fashion trend analysis endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from ..utils.fashion_trends import FashionTrendAnalyzer
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter(prefix="/trends", tags=["trends"])

# Global trend analyzer instance
trend_analyzer = FashionTrendAnalyzer()

class TrendingColor(BaseModel):
    """Trending color model."""
    color: str = Field(..., description="Color name")
    popularity: float = Field(..., description="Popularity score (0-1)")
    trend: str = Field(..., description="Trend direction (rising, stable, declining)")

class TrendingStyle(BaseModel):
    """Trending style model."""
    style: str = Field(..., description="Style name")
    popularity: float = Field(..., description="Popularity score (0-1)")
    category: str = Field(..., description="Product category")

class TrendResponse(BaseModel):
    """Trend analysis response model."""
    trending_colors: List[TrendingColor] = Field(..., description="List of trending colors")
    trending_styles: List[TrendingStyle] = Field(..., description="List of trending styles")
    timestamp: datetime = Field(default_factory=datetime.now)

@router.get(
    "/colors",
    summary="Get Trending Colors",
    description="""
    Get trending colors for fashion products.
    
    This endpoint provides information about trending colors in the fashion industry,
    including popularity scores and trend directions.
    
    **Example Response:**
    ```json
    {
        "colors": [
            {
                "color": "sage green",
                "popularity": 0.85,
                "trend": "rising"
            }
        ],
        "timeframe": "30d",
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def get_trending_colors(
    timeframe: str = Query(
        "30d",
        description="Time period for trend analysis (7d, 30d, 90d)",
        regex="^(7d|30d|90d)$"
    )
):
    """
    Get trending colors for the specified timeframe.
    
    Args:
        timeframe: Time period for trend analysis
        
    Returns:
        Dictionary containing trending colors with popularity scores
    """
    try:
        colors = trend_analyzer.get_trending_colors(timeframe)
        return {
            "colors": colors,
            "timeframe": timeframe,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending colors: {str(e)}")

@router.get(
    "/styles",
    summary="Get Trending Styles",
    description="""
    Get trending styles for fashion products.
    
    This endpoint provides information about trending styles in the fashion industry,
    filtered by product category.
    
    **Example Response:**
    ```json
    {
        "styles": [
            {
                "style": "minimalist",
                "popularity": 0.82,
                "category": "all"
            }
        ],
        "category": "all",
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def get_trending_styles(
    category: str = Query(
        "all",
        description="Product category to filter styles (all, apparel, shoes, accessories)",
        example="all"
    )
):
    """
    Get trending styles for the specified category.
    
    Args:
        category: Product category to analyze
        
    Returns:
        Dictionary containing trending styles with popularity scores
    """
    try:
        styles = trend_analyzer.get_trending_styles(category)
        return {
            "styles": styles,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending styles: {str(e)}")

@router.get(
    "/seasonal",
    summary="Get Seasonal Trends",
    description="""
    Get seasonal fashion trends.
    
    This endpoint provides information about seasonal fashion trends,
    including colors, styles, and materials for the current or specified season.
    
    **Example Response:**
    ```json
    {
        "season": "winter",
        "colors": ["navy", "black", "deep red"],
        "styles": ["coats", "sweaters", "boots"],
        "materials": ["wool", "cashmere", "leather"],
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def get_seasonal_trends(
    season: Optional[str] = Query(
        None,
        description="Season to analyze (spring, summer, fall, winter). If not specified, current season is used.",
        regex="^(spring|summer|fall|winter)$"
    )
):
    """
    Get seasonal fashion trends.
    
    Args:
        season: Season to analyze (optional, defaults to current season)
        
    Returns:
        Dictionary containing seasonal trends
    """
    try:
        trends = trend_analyzer.get_seasonal_trends(season)
        current_season = season or "current"
        return {
            "season": current_season,
            **trends,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get seasonal trends: {str(e)}")

@router.get(
    "/price",
    summary="Get Price Trends",
    description="""
    Get price trends for fashion products.
    
    This endpoint provides information about price trends in the fashion industry,
    including average prices, price changes, and category insights.
    
    **Example Response:**
    ```json
    {
        "average_price": 1500,
        "price_change": 0.05,
        "trend_direction": "increasing",
        "seasonal_adjustment": 0.1,
        "category_insights": {
            "apparel": {"avg_price": 1200, "trend": "stable"}
        },
        "category": "all",
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def get_price_trends(
    category: str = Query(
        "all",
        description="Product category to analyze",
        example="all"
    )
):
    """
    Get price trends for the specified category.
    
    Args:
        category: Product category to analyze
        
    Returns:
        Dictionary containing price trend insights
    """
    try:
        trends = trend_analyzer.get_price_trends(category)
        return {
            **trends,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get price trends: {str(e)}")

@router.get(
    "/sustainability",
    summary="Get Sustainability Trends",
    description="""
    Get sustainability trends in fashion.
    
    This endpoint provides information about sustainability trends in the fashion industry,
    including eco-friendly materials, sustainable brands, and consumer interest.
    
    **Example Response:**
    ```json
    {
        "eco_friendly_materials": ["organic cotton", "recycled polyester"],
        "sustainable_brands": ["Patagonia", "Everlane"],
        "consumer_interest": 0.75,
        "price_premium": 0.15,
        "trending_practices": ["upcycling", "rental fashion"],
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def get_sustainability_trends():
    """
    Get sustainability trends in fashion.
    
    Returns:
        Dictionary containing sustainability trend insights
    """
    try:
        trends = trend_analyzer.get_sustainability_trends()
        return {
            **trends,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sustainability trends: {str(e)}")

@router.get(
    "/report",
    summary="Get Comprehensive Trend Report",
    description="""
    Get a comprehensive fashion trend report.
    
    This endpoint provides a complete trend analysis including:
    - Trending colors
    - Trending styles
    - Seasonal trends
    - Price trends
    - Sustainability trends
    
    **Example Response:**
    ```json
    {
        "timestamp": "2024-01-15T10:30:00",
        "trending_colors": [...],
        "trending_styles": [...],
        "seasonal_trends": {...},
        "price_trends": {...},
        "sustainability_trends": {...}
    }
    ```
    """,
    response_model=dict
)
async def get_trend_report():
    """
    Get a comprehensive fashion trend report.
    
    Returns:
        Dictionary containing all trend insights
    """
    try:
        report = trend_analyzer.generate_trend_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate trend report: {str(e)}")

@router.post(
    "/brands",
    summary="Analyze Brand Performance",
    description="""
    Analyze performance metrics for specified brands.
    
    This endpoint provides brand performance analysis including:
    - Popularity scores
    - Price ranges
    - Trending products
    - Customer satisfaction
    
    **Example Request:**
    ```json
    {
        "brands": ["nike", "adidas", "zara"]
    }
    ```
    
    **Example Response:**
    ```json
    {
        "nike": {
            "popularity_score": 0.85,
            "price_range": "premium",
            "trending_products": ["shirt", "jeans"],
            "customer_satisfaction": 0.88
        },
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    response_model=dict
)
async def analyze_brand_performance(brands: List[str] = Body(..., description="List of brand names to analyze", example=["nike", "adidas", "zara"])):
    """
    Analyze performance metrics for specified brands.
    
    Args:
        brands: List of brand names to analyze
        
    Returns:
        Dictionary containing brand performance metrics
    """
    try:
        if not brands:
            raise HTTPException(status_code=400, detail="Brands list cannot be empty")
        
        performance = trend_analyzer.analyze_brand_performance(brands)
        return {
            **performance,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze brand performance: {str(e)}")

