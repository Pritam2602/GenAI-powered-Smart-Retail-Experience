"""
Pydantic data models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class PriceRequest(BaseModel):
    """Request model for price prediction."""
    product_name: str = Field(..., description="Name of the product")
    brand: str = Field(..., description="Brand of the product")
    gender: str = Field(..., description="Target gender (men, women, unisex, boys, girls)")
    category: str = Field(..., description="Product category")
    fabric: Optional[str] = Field(None, description="Fabric type")
    pattern: Optional[str] = Field(None, description="Pattern type")
    color: Optional[str] = Field(None, description="Color")
    rating_count: int = Field(0, ge=0, description="Number of ratings")
    discount_percent: float = Field(0.0, ge=0.0, le=100.0, description="Discount percentage")

class SearchRequest(BaseModel):
    """Request model for product search/recommendation."""
    query: str = Field(..., description="Search query text")
    k: int = Field(10, ge=1, le=50, description="Number of results to return")

class PredictionResponse(BaseModel):
    """Response model for price prediction."""
    predicted_price: float = Field(..., description="Predicted price in INR")
    product_type: str = Field(..., description="Classified product type")
    model_type: str = Field(..., description="Type of model used")
    confidence: str = Field(..., description="Confidence level")
    timestamp: datetime = Field(default_factory=datetime.now)

class RecommendationItem(BaseModel):
    """Individual recommendation item."""
    id: str = Field(..., description="Product ID")
    document: str = Field(..., description="Product description")
    metadata: Dict[str, Any] = Field(..., description="Product metadata")
    distance: Optional[float] = Field(None, description="Similarity distance")
    score: Optional[float] = Field(None, description="Recommendation score")

class RecommendationResponse(BaseModel):
    """Response model for product recommendations."""
    results: List[RecommendationItem] = Field(..., description="List of recommended products")
    query: str = Field(..., description="Original search query")
    total_results: int = Field(..., description="Total number of results")
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    fast_models_loaded: bool = Field(..., description="Fast models availability")
    original_model_loaded: bool = Field(..., description="Original model availability")
    recs_index_loaded: bool = Field(..., description="Recommendation index availability")
    recs_count: int = Field(..., description="Number of items in recommendation index")
    embedding_model_loaded: bool = Field(..., description="Embedding model availability")
    model_type_in_use: str = Field(..., description="Currently active model type")
    timestamp: datetime = Field(default_factory=datetime.now)
