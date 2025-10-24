"""
Price prediction endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, HTTPException, Depends
from ..models.data_models import PriceRequest, PredictionResponse
from ..models.ml_models import ModelManager

router = APIRouter(prefix="/predict", tags=["price-prediction"])

# Global model manager instance
model_manager = ModelManager()

@router.post("/price", response_model=PredictionResponse)
async def predict_price(request: PriceRequest):
    """
    Predict the price of a fashion item using AI models.
    
    Args:
        request: Product details for price prediction
        
    Returns:
        PredictionResponse: Predicted price and model information
        
    Raises:
        HTTPException: If no models are loaded or prediction fails
    """
    try:
        # Convert request to dict
        product_data = request.dict()
        
        # Get prediction
        prediction = model_manager.predict_price(product_data)
        
        # Determine confidence level
        product_type = prediction.get('product_type', 'apparel')
        confidence = "High" if product_type in ['jewelry', 'watches'] else "Medium"
        
        return PredictionResponse(
            predicted_price=prediction['predicted_price'],
            product_type=prediction.get('product_type', 'apparel'),
            model_type=prediction['model_type'],
            confidence=confidence
        )
        
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
