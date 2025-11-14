"""
Explainability utilities for price prediction models.
Provides feature importance and explanation insights.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

class PricePredictionExplainer:
    """Explains price predictions using feature importance."""
    
    @staticmethod
    def get_feature_importance(product_data: Dict[str, Any], model, feature_names: List[str]) -> Dict[str, float]:
        """
        Get feature importance for a product prediction.
        
        Args:
            product_data: Product data dictionary
            model: Trained model (must have feature_importances_ attribute)
            feature_names: List of feature names
            
        Returns:
            Dictionary of feature importance scores
        """
        try:
            # Check if model has feature_importances_ attribute
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                # Create dictionary mapping feature names to importance scores
                feature_importance = dict(zip(feature_names, importances))
                # Sort by importance
                feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
                return feature_importance
            else:
                # For pipeline models, try to get feature importance from the regressor
                if hasattr(model, 'steps') and len(model.steps) > 0:
                    # Get the regressor step
                    regressor = model.steps[-1][1]
                    if hasattr(regressor, 'feature_importances_'):
                        importances = regressor.feature_importances_
                        feature_importance = dict(zip(feature_names, importances))
                        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
                        return feature_importance
        except Exception as e:
            print(f"Could not get feature importance: {e}")
        
        # Return empty dictionary if feature importance is not available
        return {}
    
    @staticmethod
    def explain_prediction(product_data: Dict[str, Any], predicted_price: float, 
                          model_type: str, product_type: str) -> Dict[str, Any]:
        """
        Generate explanation for a price prediction.
        
        Args:
            product_data: Product data dictionary
            predicted_price: Predicted price
            model_type: Type of model used
            product_type: Product type classification
            
        Returns:
            Dictionary containing explanation details
        """
        explanation = {
            "predicted_price": predicted_price,
            "model_type": model_type,
            "product_type": product_type,
            "key_factors": [],
            "feature_contributions": {},
            "price_breakdown": {},
            "recommendations": []
        }
        
        # Extract key factors
        key_factors = []
        
        # Brand impact
        brand = product_data.get('brand', '').lower()
        if brand:
            key_factors.append({
                "factor": "Brand",
                "value": brand,
                "impact": "high" if brand in ['nike', 'adidas', 'zara'] else "medium",
                "description": f"Brand {brand} has a significant impact on price"
            })
        
        # Category impact
        category = product_data.get('category', '').lower()
        if category:
            category_impact = {
                "shoes": "high",
                "dress": "medium-high",
                "jeans": "medium",
                "shirt": "medium",
                "jacket": "high"
            }.get(category, "medium")
            key_factors.append({
                "factor": "Category",
                "value": category,
                "impact": category_impact,
                "description": f"Category {category} affects price range"
            })
        
        # Discount impact
        discount = product_data.get('discount_percent', 0)
        if discount > 0:
            discount_impact = predicted_price * (discount / 100)
            key_factors.append({
                "factor": "Discount",
                "value": f"{discount}%",
                "impact": "high" if discount > 30 else "medium",
                "description": f"{discount}% discount reduces price by approximately ₹{discount_impact:.2f}"
            })
        
        # Material impact
        fabric = product_data.get('fabric', '').lower()
        if fabric:
            material_impact = {
                "silk": "high",
                "cashmere": "high",
                "leather": "high",
                "wool": "medium-high",
                "cotton": "medium",
                "polyester": "low"
            }.get(fabric, "medium")
            key_factors.append({
                "factor": "Material",
                "value": fabric,
                "impact": material_impact,
                "description": f"Material {fabric} affects price"
            })
        
        # Rating count impact
        rating_count = product_data.get('rating_count', 0)
        if rating_count > 0:
            rating_impact = "high" if rating_count > 500 else "medium" if rating_count > 100 else "low"
            key_factors.append({
                "factor": "Rating Count",
                "value": rating_count,
                "impact": rating_impact,
                "description": f"Product has {rating_count} ratings, indicating popularity"
            })
        
        explanation["key_factors"] = key_factors
        
        # Price breakdown
        base_price = predicted_price
        if discount > 0:
            original_price = base_price / (1 - discount / 100)
            explanation["price_breakdown"] = {
                "original_price": round(original_price, 2),
                "discount_amount": round(original_price - base_price, 2),
                "discount_percent": discount,
                "final_price": round(base_price, 2)
            }
        else:
            explanation["price_breakdown"] = {
                "original_price": round(base_price, 2),
                "discount_amount": 0,
                "discount_percent": 0,
                "final_price": round(base_price, 2)
            }
        
        # Recommendations
        recommendations = []
        
        # Price range recommendations
        if product_type == "apparel":
            if predicted_price > 5000:
                recommendations.append("Consider premium materials or designer brands")
            elif predicted_price < 1000:
                recommendations.append("Budget-friendly option with good value")
        
        # Discount recommendations
        if discount == 0:
            recommendations.append("No discount applied - consider seasonal sales")
        elif discount > 50:
            recommendations.append("High discount - good value for money")
        
        # Brand recommendations
        if brand in ['nike', 'adidas']:
            recommendations.append("Premium brand - expect higher prices")
        elif brand in ['roadster', 'h&m']:
            recommendations.append("Budget-friendly brand - good value")
        
        explanation["recommendations"] = recommendations
        
        return explanation
    
    @staticmethod
    def get_similar_products_price_range(product_data: Dict[str, Any], 
                                        similar_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get price range for similar products.
        
        Args:
            product_data: Product data dictionary
            similar_products: List of similar products with prices
            
        Returns:
            Dictionary containing price range statistics
        """
        if not similar_products:
            return {
                "min_price": 0,
                "max_price": 0,
                "avg_price": 0,
                "median_price": 0,
                "count": 0
            }
        
        prices = [p.get('price', 0) for p in similar_products if 'price' in p]
        
        if not prices:
            return {
                "min_price": 0,
                "max_price": 0,
                "avg_price": 0,
                "median_price": 0,
                "count": 0
            }
        
        return {
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2),
            "avg_price": round(np.mean(prices), 2),
            "median_price": round(np.median(prices), 2),
            "count": len(prices)
        }
    
    @staticmethod
    def compare_with_market_average(predicted_price: float, market_avg: float) -> Dict[str, Any]:
        """
        Compare predicted price with market average.
        
        Args:
            predicted_price: Predicted price
            market_avg: Market average price
            
        Returns:
            Dictionary containing comparison results
        """
        difference = predicted_price - market_avg
        difference_percent = (difference / market_avg) * 100 if market_avg > 0 else 0
        
        return {
            "predicted_price": round(predicted_price, 2),
            "market_average": round(market_avg, 2),
            "difference": round(difference, 2),
            "difference_percent": round(difference_percent, 2),
            "status": "above_average" if difference > 0 else "below_average" if difference < 0 else "average",
            "description": f"Predicted price is {abs(difference_percent):.2f}% {'above' if difference > 0 else 'below'} market average"
        }

