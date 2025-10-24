"""
Data preprocessing and feature extraction utilities.
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

class DataPreprocessor:
    """Handles data cleaning and preprocessing for fashion data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text data."""
        if not isinstance(text, str):
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-\.]', '', text)
        
        return text.lower()
    
    @staticmethod
    def normalize_brand(brand: str) -> str:
        """Normalize brand names."""
        if not isinstance(brand, str):
            return "unknown"
        
        brand = brand.lower().strip()
        
        # Common brand variations
        brand_mappings = {
            'h&m': 'h&m',
            'hm': 'h&m',
            'zara': 'zara',
            'nike': 'nike',
            'adidas': 'adidas',
            'puma': 'puma',
            'rebook': 'reebok',
            'reebok': 'reebok'
        }
        
        return brand_mappings.get(brand, brand)
    
    @staticmethod
    def normalize_category(category: str) -> str:
        """Normalize product categories."""
        if not isinstance(category, str):
            return "other"
        
        category = category.lower().strip()
        
        # Category mappings
        category_mappings = {
            'shirt': 'shirt',
            'tshirt': 'shirt',
            't-shirt': 'shirt',
            'top': 'shirt',
            'jeans': 'jeans',
            'pants': 'jeans',
            'trousers': 'jeans',
            'dress': 'dress',
            'gown': 'dress',
            'shoes': 'shoes',
            'footwear': 'shoes',
            'sneakers': 'shoes',
            'jacket': 'jacket',
            'coat': 'jacket',
            'blazer': 'jacket'
        }
        
        return category_mappings.get(category, category)
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # Fill missing text fields
        text_columns = ['product_name', 'brand', 'category', 'fabric', 'pattern', 'color']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('unknown')
        
        # Fill missing numerical fields
        numerical_columns = ['rating_count', 'discount_percent']
        for col in numerical_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        return df

class FeatureExtractor:
    """Extracts features from product data for ML models."""
    
    MATERIAL_KEYWORDS = [
        'cotton', 'polyester', 'silk', 'wool', 'denim', 'leather', 'cashmere', 
        'pashmina', 'georgette', 'velvet', 'linen', 'chiffon', 'organza', 'net', 'lace'
    ]
    
    STYLE_KEYWORDS = [
        'casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 
        'traditional', 'vintage', 'retro', 'modern', 'classic', 'trendy', 'elegant', 'chic'
    ]
    
    LUXURY_KEYWORDS = [
        'designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
        'embroidered', 'sequined', 'beaded', 'crystal', 'swarovski'
    ]
    
    @classmethod
    def extract_basic_features(cls, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic features from product data."""
        product_name = str(product_data.get('product_name', ''))
        
        features = {
            'name_length': len(product_name),
            'word_count': len(product_name.split()),
            'has_discount': float(product_data.get('discount_percent', 0)) > 0,
            'rating_count': int(product_data.get('rating_count', 0)),
            'discount_percent': float(product_data.get('discount_percent', 0))
        }
        
        return features
    
    @classmethod
    def extract_material_features(cls, product_data: Dict[str, Any]) -> Dict[str, bool]:
        """Extract material-related features."""
        product_name = str(product_data.get('product_name', '')).lower()
        fabric = str(product_data.get('fabric', '')).lower()
        
        features = {}
        for material in cls.MATERIAL_KEYWORDS:
            features[f'has_{material}'] = (
                material in product_name or 
                material in fabric
            )
        
        return features
    
    @classmethod
    def extract_style_features(cls, product_data: Dict[str, Any]) -> Dict[str, bool]:
        """Extract style-related features."""
        product_name = str(product_data.get('product_name', '')).lower()
        
        features = {}
        for style in cls.STYLE_KEYWORDS:
            features[f'has_{style}'] = style in product_name
        
        return features
    
    @classmethod
    def extract_luxury_features(cls, product_data: Dict[str, Any]) -> Dict[str, bool]:
        """Extract luxury-related features."""
        product_name = str(product_data.get('product_name', '')).lower()
        
        features = {}
        for keyword in cls.LUXURY_KEYWORDS:
            features[f'luxury_{keyword}'] = keyword in product_name
        
        return features
    
    @classmethod
    def extract_size_features(cls, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract size-related features."""
        product_name = str(product_data.get('product_name', '')).lower()
        
        # Size keywords
        size_keywords = ['xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl', 'small', 'medium', 'large']
        has_size = any(size in product_name for size in size_keywords)
        
        # Size pattern matching
        size_pattern = re.search(r'\b(?:xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', product_name, re.IGNORECASE)
        
        return {
            'has_size': has_size,
            'size_mentioned': bool(size_pattern)
        }
    
    @classmethod
    def extract_brand_features(cls, product_data: Dict[str, Any], brand_prestige_scores: Dict[str, float]) -> Dict[str, Any]:
        """Extract brand-related features."""
        brand = str(product_data.get('brand', '')).lower()
        avg_price = brand_prestige_scores.get(brand, 0)
        
        # Brand prestige categories
        if avg_price >= 5000:
            prestige = 'ultra_premium'
        elif avg_price >= 2000:
            prestige = 'premium'
        elif avg_price >= 500:
            prestige = 'mid_range'
        else:
            prestige = 'budget'
        
        return {
            'brand_avg_price': avg_price,
            'brand_prestige': prestige,
            'is_premium_brand': avg_price >= 2000
        }
    
    @classmethod
    def extract_all_features(cls, product_data: Dict[str, Any], brand_prestige_scores: Dict[str, float]) -> Dict[str, Any]:
        """Extract all features from product data."""
        features = {}
        
        # Basic features
        features.update(cls.extract_basic_features(product_data))
        
        # Material features
        features.update(cls.extract_material_features(product_data))
        
        # Style features
        features.update(cls.extract_style_features(product_data))
        
        # Luxury features
        features.update(cls.extract_luxury_features(product_data))
        
        # Size features
        features.update(cls.extract_size_features(product_data))
        
        # Brand features
        features.update(cls.extract_brand_features(product_data, brand_prestige_scores))
        
        return features
