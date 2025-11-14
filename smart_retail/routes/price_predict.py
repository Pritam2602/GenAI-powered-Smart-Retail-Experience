"""
Price prediction endpoints for the Smart Retail API.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.data_models import PriceRequest, PredictionResponse
from ..models.ml_models import ModelManager
from ..utils.explainability import PricePredictionExplainer

router = APIRouter(prefix="/predict", tags=["price-prediction"])

# Global model manager instance
model_manager = ModelManager()

@router.post(
    "/price",
    response_model=PredictionResponse,
    summary="Predict Product Price",
    description="""
    Predict the price of a fashion item using AI models.
    
    This endpoint uses specialized ML models based on product type:
    - **Jewelry Model**: For gold, silver, diamonds, precious stones
    - **Watch Model**: For timepieces, movements, luxury brands
    - **Luxury Apparel Model**: For designer, premium, high-end fashion
    - **Standard Apparel Model**: For regular clothing and accessories
    
    The system automatically classifies the product type based on the input
    and selects the appropriate model for accurate price prediction.
    
    **Features:**
    - Automatic product type classification
    - Specialized models for different product types
    - Optional explanation generation (set `explain=true` query parameter)
    - Feature importance and key factors analysis
    
    **Example Request:**
    ```json
    {
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
    ```
    
    **Example Response (without explanation):**
    ```json
    {
        "predicted_price": 899.50,
        "product_type": "apparel",
        "model_type": "fast_multi_model",
        "confidence": "Medium",
        "timestamp": "2024-01-15T10:30:00",
        "explanation": null
    }
    ```
    
    **Example Response (with explanation - add `?explain=true`):**
    ```json
    {
        "predicted_price": 899.50,
        "product_type": "apparel",
        "model_type": "fast_multi_model",
        "confidence": "Medium",
        "timestamp": "2024-01-15T10:30:00",
        "explanation": {
            "key_factors": [
                {
                    "factor": "Brand",
                    "value": "roadster",
                    "impact": "medium",
                    "description": "Brand roadster has a significant impact on price"
                },
                {
                    "factor": "Discount",
                    "value": "40%",
                    "impact": "high",
                    "description": "40% discount reduces price by approximately ₹359.80"
                }
            ],
            "price_breakdown": {
                "original_price": 1499.17,
                "discount_amount": 599.67,
                "discount_percent": 40.0,
                "final_price": 899.50
            },
            "recommendations": [
                "Budget-friendly brand - good value",
                "High discount - good value for money"
            ]
        }
    }
    ```
    """,
    responses={
        200: {
            "description": "Successful price prediction",
            "content": {
                "application/json": {
                    "example": {
                        "predicted_price": 899.50,
                        "product_type": "apparel",
                        "model_type": "fast_multi_model",
                        "confidence": "Medium",
                        "timestamp": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        503: {
            "description": "Service unavailable - no models loaded",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No price models are loaded"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Prediction failed: <error message>"
                    }
                }
            }
        }
    }
)
async def predict_price(
    request: PriceRequest,
    explain: bool = Query(
        False,
        description="Generate explanation for the prediction (shows key factors and feature contributions)",
        example=False
    )
):
    """
    Predict the price of a fashion item using AI models.
    
    Args:
        request: Product details for price prediction
        explain: Whether to generate explanation for the prediction
        
    Returns:
        PredictionResponse: Predicted price and model information (with explanation if requested)
        
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
        
        # Generate explanation if requested
        explanation = None
        if explain:
            try:
                explanation = PricePredictionExplainer.explain_prediction(
                    product_data=product_data,
                    predicted_price=prediction['predicted_price'],
                    model_type=prediction['model_type'],
                    product_type=prediction.get('product_type', 'apparel')
                )
            except Exception as e:
                # If explanation fails, continue without it
                print(f"Could not generate explanation: {e}")
                explanation = None
        
        return PredictionResponse(
            predicted_price=prediction['predicted_price'],
            product_type=prediction.get('product_type', 'apparel'),
            model_type=prediction['model_type'],
            confidence=confidence,
            explanation=explanation
        )
        
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
