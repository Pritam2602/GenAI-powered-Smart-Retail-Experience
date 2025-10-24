"""
Product recommendation endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, HTTPException
from ..models.data_models import SearchRequest, RecommendationResponse, RecommendationItem
from ..models.ml_models import ModelManager

router = APIRouter(prefix="/recommend", tags=["recommendations"])

# Global model manager instance
model_manager = ModelManager()

@router.post("/products", response_model=RecommendationResponse)
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
