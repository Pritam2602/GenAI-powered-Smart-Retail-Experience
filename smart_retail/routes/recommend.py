"""
Product recommendation endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, HTTPException
from ..models.data_models import SearchRequest, RecommendationResponse, RecommendationItem
from ..models.ml_models import ModelManager

router = APIRouter(prefix="/recommend", tags=["recommendations"])

# Global model manager instance
model_manager = ModelManager()

@router.post(
    "/products",
    response_model=RecommendationResponse,
    summary="Get Product Recommendations",
    description="""
    Recommend similar fashion items based on a text query using semantic search.
    
    This endpoint uses sentence transformers to encode the query and find
    similar products in the vector database using cosine similarity.
    
    **Features:**
    - Semantic search using sentence transformers
    - Vector-based similarity matching
    - Configurable number of results (1-50)
    - Returns products with similarity scores
    
    **Example Request:**
    ```json
    {
        "query": "blue denim jacket for men",
        "k": 10
    }
    ```
    
    **Example Response:**
    ```json
    {
        "results": [
            {
                "id": "product_123",
                "document": "Men Blue Denim Jacket",
                "metadata": {
                    "brand": "roadster",
                    "price": 1299,
                    "rating": 4.2
                },
                "distance": 0.15,
                "score": 0.85
            }
        ],
        "query": "blue denim jacket for men",
        "total_results": 10,
        "timestamp": "2024-01-15T10:30:00"
    }
    ```
    """,
    responses={
        200: {
            "description": "Successful recommendation",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "id": "product_123",
                                "document": "Men Blue Denim Jacket",
                                "metadata": {
                                    "brand": "roadster",
                                    "price": 1299,
                                    "rating": 4.2
                                },
                                "distance": 0.15,
                                "score": 0.85
                            }
                        ],
                        "query": "blue denim jacket for men",
                        "total_results": 1,
                        "timestamp": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        503: {
            "description": "Service unavailable - recommendation system not available",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Recommendation system is not available"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Recommendation query failed: <error message>"
                    }
                }
            }
        }
    }
)
async def recommend_products(request: SearchRequest):
    """
    Recommend similar fashion items based on a text query.
    
    Args:
        request: Search query and number of results
        
    Returns:
        RecommendationResponse: List of recommended products
        
    Raises:
        HTTPException: If recommendation system is not available
    """
    try:
        # Get recommendations
        recommendations = model_manager.get_recommendations(
            query=request.query,
            k=request.k
        )
        
        # Convert to response format
        items = []
        for item in recommendations.get('results', []):
            items.append(RecommendationItem(
                id=item['id'],
                document=item['document'],
                metadata=item['metadata'],
                distance=item.get('distance'),
                score=1.0 - item.get('distance', 0) if item.get('distance') else None
            ))
        
        return RecommendationResponse(
            results=items,
            query=request.query,
            total_results=len(items)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation query failed: {str(e)}")
