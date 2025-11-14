"""
Input validation utilities for the Smart Retail system.
"""

import re
from typing import Dict, Any, List, Optional
from ..config import settings

class InputValidator:
    """Validates input data for the Smart Retail API."""
    
    VALID_GENDERS = ["men", "women", "unisex", "boys", "girls"]
    VALID_CATEGORIES = [
        "shirt", "jeans", "dress", "shoes", "jacket", "top", "bottom", 
        "accessories", "jewelry", "watch", "bag", "hat"
    ]
    VALID_MATERIALS = [
        "cotton", "polyester", "silk", "wool", "denim", "leather", 
        "cashmere", "linen", "chiffon", "organza", "velvet"
    ]
    VALID_PATTERNS = [
        "solid", "striped", "printed", "floral", "geometric", 
        "abstract", "polka dot", "checkered"
    ]
    
    @classmethod
    def validate_price_request(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate price prediction request data.
        
        Args:
            data: Request data to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ["product_name", "brand", "gender", "category"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate gender
        if data.get("gender") and data["gender"] not in cls.VALID_GENDERS:
            errors.append(f"Invalid gender. Must be one of: {', '.join(cls.VALID_GENDERS)}")
        
        # Validate category
        if data.get("category") and data["category"].lower() not in [c.lower() for c in cls.VALID_CATEGORIES]:
            errors.append(f"Invalid category. Must be one of: {', '.join(cls.VALID_CATEGORIES)}")
        
        # Validate numerical fields
        if data.get("rating_count") is not None:
            try:
                rating_count = int(data["rating_count"])
                if rating_count < 0:
                    errors.append("rating_count must be non-negative")
            except (ValueError, TypeError):
                errors.append("rating_count must be a valid integer")
        
        if data.get("discount_percent") is not None:
            try:
                discount = float(data["discount_percent"])
                if not 0 <= discount <= 100:
                    errors.append("discount_percent must be between 0 and 100")
            except (ValueError, TypeError):
                errors.append("discount_percent must be a valid number")
        
        # Validate text fields
        if data.get("product_name"):
            if len(data["product_name"]) > 200:
                errors.append("product_name must be 200 characters or less")
        
        if data.get("brand"):
            if len(data["brand"]) > 50:
                errors.append("brand must be 50 characters or less")
        
        return errors
    
    @classmethod
    def validate_search_request(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate product search request data.
        
        Args:
            data: Request data to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate query
        if not data.get("query"):
            errors.append("Missing required field: query")
        elif len(data["query"]) > 500:
            errors.append("query must be 500 characters or less")
        
        # Validate k parameter
        if data.get("k") is not None:
            try:
                k = int(data["k"])
                if not 1 <= k <= 50:
                    errors.append("k must be between 1 and 50")
            except (ValueError, TypeError):
                errors.append("k must be a valid integer")
        
        return errors
    
    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Sanitize text input to prevent injection attacks.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove potentially dangerous characters
        text = re.sub(r'[<>"\']', '', text)
        
        # Limit length
        text = text[:1000]
        
        return text.strip()
    
    @classmethod
    def validate_product_data(cls, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize product data.
        
        Args:
            product_data: Product data to validate
            
        Returns:
            Validated and sanitized product data
        """
        validated_data = {}
        
        # Sanitize text fields
        text_fields = ["product_name", "brand", "category", "fabric", "pattern", "color"]
        for field in text_fields:
            if field in product_data:
                validated_data[field] = cls.sanitize_text(str(product_data[field]))
        
        # Validate and convert numerical fields
        if "rating_count" in product_data:
            try:
                validated_data["rating_count"] = max(0, int(product_data["rating_count"]))
            except (ValueError, TypeError):
                validated_data["rating_count"] = 0
        
        if "discount_percent" in product_data:
            try:
                discount = float(product_data["discount_percent"])
                validated_data["discount_percent"] = max(0, min(100, discount))
            except (ValueError, TypeError):
                validated_data["discount_percent"] = 0.0
        
        return validated_data
    
    @classmethod
    def is_valid_brand(cls, brand: str) -> bool:
        """
        Check if brand name is valid.
        
        Args:
            brand: Brand name to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not brand or not isinstance(brand, str):
            return False
        
        # Check length
        if len(brand) > 50:
            return False
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s\&\-\.]+$', brand):
            return False
        
        return True
    
    @classmethod
    def is_valid_price(cls, price: float) -> bool:
        """
        Check if price is valid.
        
        Args:
            price: Price to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            price_float = float(price)
            return 0 <= price_float <= 1000000  # Max 1M INR
        except (ValueError, TypeError):
            return False
