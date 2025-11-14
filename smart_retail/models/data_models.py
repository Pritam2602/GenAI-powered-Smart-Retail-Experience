"""
Pydantic data models for request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class PriceRequest(BaseModel):
    """Request model for price prediction."""
    product_name: str = Field(
        ...,
        description="Name of the product",
        example="Men Solid Casual Shirt",
        min_length=1,
        max_length=500
    )
    brand: str = Field(
        ...,
        description="Brand of the product",
        example="roadster",
        min_length=1,
        max_length=100
    )
    gender: str = Field(
        ...,
        description="Target gender (men, women, unisex, boys, girls)",
        example="men"
    )
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender field."""
        valid_genders = ['men', 'women', 'unisex', 'boys', 'girls']
        v_lower = v.lower()
        if v_lower not in valid_genders:
            raise ValueError(f'Gender must be one of: {", ".join(valid_genders)}')
        return v_lower
    category: str = Field(
        ...,
        description="Product category (e.g., shirt, jeans, dress, shoes, jacket)",
        example="shirt",
        min_length=1,
        max_length=100
    )
    fabric: Optional[str] = Field(
        None,
        description="Fabric type (e.g., cotton, polyester, silk, denim)",
        example="cotton",
        max_length=100
    )
    pattern: Optional[str] = Field(
        None,
        description="Pattern type (e.g., solid, striped, printed, checked)",
        example="solid",
        max_length=100
    )
    color: Optional[str] = Field(
        None,
        description="Color of the product",
        example="blue",
        max_length=50
    )
    rating_count: int = Field(
        0,
        ge=0,
        description="Number of ratings/reviews",
        example=500
    )
    discount_percent: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Discount percentage (0-100)",
        example=40.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "product_name": "Men Solid Casual Shirt",
                "brand": "roadster",
                "gender": "men",
                "category": "shirt",
                "fabric": "cotton",
                "pattern": "solid",
                "color": "blue",
                "rating_count": 500,
                "discount_percent": 40.0
            }
        }

class SearchRequest(BaseModel):
    """Request model for product search/recommendation."""
    query: str = Field(
        ...,
        description="Search query text (e.g., 'blue denim jacket for men')",
        example="blue denim jacket for men",
        min_length=1,
        max_length=500
    )
    k: int = Field(
        10,
        ge=1,
        le=50,
        description="Number of results to return (1-50)",
        example=10
    )
    
    class Config:
        schema_extra = {
            "example": {
                "query": "blue denim jacket for men",
                "k": 10
            }
        }

class PredictionResponse(BaseModel):
    """Response model for price prediction."""
    predicted_price: float = Field(
        ...,
        description="Predicted price in INR",
        example=899.50,
        ge=0
    )
    product_type: str = Field(
        ...,
        description="Classified product type (jewelry, watches, luxury_apparel, apparel)",
        example="apparel"
    )
    model_type: str = Field(
        ...,
        description="Type of model used (fast_multi_model, original_single_model, fallback_model)",
        example="fast_multi_model"
    )
    confidence: str = Field(
        ...,
        description="Confidence level (High, Medium, Low)",
        example="Medium"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of the prediction"
    )
    explanation: Optional[Dict[str, Any]] = Field(
        None,
        description="Explanation of the prediction (optional, requires explain=True in request)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "predicted_price": 899.50,
                "product_type": "apparel",
                "model_type": "fast_multi_model",
                "confidence": "Medium",
                "timestamp": "2024-01-15T10:30:00",
                "explanation": None
            }
        }

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
