"""
ML Model management and product classification.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import re

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from ..config import settings

class ProductClassifier:
    """Classifies products into different types for specialized model selection."""
    
    JEWELRY_KEYWORDS = [
        'ring', 'chain', 'earring', 'necklace', 'bracelet', 'pendant', 'bangle', 
        'diamond', 'gold', 'silver', 'platinum', 'karat', 'kt', 'gem', 'stone'
    ]
    
    WATCH_KEYWORDS = [
        'watch', 'chronograph', 'automatic', 'quartz', 'movement', 'dial', 'strap',
        'timepiece', 'wristwatch', 'casio', 'titan', 'fastrack', 'fossil'
    ]
    
    LUXURY_KEYWORDS = [
        'designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
        'cashmere', 'silk', 'leather', 'wool', 'pashmina', 'georgette', 'velvet'
    ]
    
    @classmethod
    def classify_product_type(cls, product_data: Dict[str, Any]) -> str:
        """Classify products into different types based on category and keywords."""
        category = str(product_data.get('category', '')).lower()
        product_name = str(product_data.get('product_name', '')).lower()
        
        if any(keyword in category or keyword in product_name for keyword in cls.JEWELRY_KEYWORDS):
            return 'jewelry'
        elif any(keyword in category or keyword in product_name for keyword in cls.WATCH_KEYWORDS):
            return 'watches'
        elif any(keyword in product_name for keyword in cls.LUXURY_KEYWORDS):
            return 'luxury_apparel'
        else:
            return 'apparel'

class ModelManager:
    """Manages loading and prediction with multiple ML models."""
    
    def __init__(self):
        self.fast_models = None
        self.original_model = None
        self.rec_collection = None
        self.embedding_model = None
        self._load_models()
    
    def _load_models(self):
        """Load all available models."""
        self._load_price_models()
        self._load_recommendation_models()
    
    def _load_price_models(self):
        """Load price prediction models."""
        # Ensure artifacts directory exists
        settings.ensure_directories()
        
        # Try to load fast multi-model system
        if settings.FAST_MODELS_PATH.exists():
            try:
                self.fast_models = joblib.load(settings.FAST_MODELS_PATH)
                print("Fast multi-model system loaded successfully")
            except Exception as e:
                print(f"Could not load fast models: {e}")
        
        # Fallback to original model
        if not self.fast_models and settings.ORIGINAL_MODEL_PATH.exists():
            try:
                model_data = joblib.load(settings.ORIGINAL_MODEL_PATH)
                self.original_model = model_data['pipeline']
                print("Original model loaded as fallback")
            except Exception as e:
                print(f"Could not load original model: {e}")
        
        # Final fallback to lightweight model
        if not self.fast_models and not self.original_model and settings.FALLBACK_MODEL_PATH.exists():
            try:
                model_data = joblib.load(settings.FALLBACK_MODEL_PATH)
                self.original_model = model_data['pipeline']
                print("Fallback model loaded successfully")
            except Exception as e:
                print(f"Could not load fallback model: {e}")
        
        # Create simple model if none available
        if not self.fast_models and not self.original_model:
            self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create a simple fallback model if no models are available."""
        try:
            print("Creating simple fallback model...")
            
            # Create synthetic dataset
            np.random.seed(42)
            n_samples = 500
            
            data = {
                'brand': np.random.choice(['roadster', 'h&m', 'zara', 'nike', 'adidas'], n_samples),
                'gender': np.random.choice(['men', 'women'], n_samples),
                'category': np.random.choice(['shirt', 'jeans', 'dress', 'shoes'], n_samples),
                'fabric': np.random.choice(['cotton', 'polyester', 'denim', 'silk'], n_samples),
                'pattern': np.random.choice(['solid', 'striped', 'printed'], n_samples),
                'color': np.random.choice(['blue', 'black', 'white', 'red'], n_samples),
                'number_of_ratings': np.random.randint(10, 1000, n_samples),
                'discount_percentage': np.random.uniform(0, 70, n_samples)
            }
            
            df = pd.DataFrame(data)
            
            # Simple price calculation
            base_price = 1000
            brand_multiplier = {'nike': 1.5, 'adidas': 1.4, 'zara': 1.2, 'h&m': 1.0, 'roadster': 0.8}
            category_multiplier = {'shoes': 1.3, 'dress': 1.2, 'jeans': 1.1, 'shirt': 1.0}
            
            prices = []
            for _, row in df.iterrows():
                price = base_price
                price *= brand_multiplier.get(row['brand'], 1.0)
                price *= category_multiplier.get(row['category'], 1.0)
                price *= (1 - row['discount_percentage'] / 100)
                price += np.random.normal(0, 100)
                prices.append(max(100, price))
            
            df['price'] = prices
            
            # Prepare features
            feature_columns = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color', 'number_of_ratings', 'discount_percentage']
            X = df[feature_columns]
            y = df['price']
            
            # Create model
            categorical_features = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color']
            numerical_features = ['number_of_ratings', 'discount_percentage']
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), numerical_features),
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
                ]
            )
            
            model = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=20, random_state=42))
            ])
            
            model.fit(X, y)
            self.original_model = model
            print("Simple fallback model created successfully")
            
        except Exception as e:
            print(f"Could not create fallback model: {e}")
    
    def _load_recommendation_models(self):
        """Load recommendation models (ChromaDB and SentenceTransformer)."""
        if not CHROMADB_AVAILABLE:
            print("ChromaDB not available, recommendation system disabled")
            return
        
        try:
            # Load embedding model
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            print("SentenceTransformer embedding model loaded")
            
            # Connect to ChromaDB
            chroma_client = chromadb.PersistentClient(path=str(settings.CHROMA_DB_DIR))
            self.rec_collection = chroma_client.get_collection(settings.CHROMA_COLLECTION_NAME)
            
            try:
                rec_count = self.rec_collection.count()
                print(f"ChromaDB collection loaded successfully (items: {rec_count})")
            except Exception:
                print("ChromaDB collection loaded but empty")
                
        except Exception as e:
            print(f"Could not load recommendation models: {e}")
            self.rec_collection = None
            self.embedding_model = None
    
    def predict_price(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict price using the best available model."""
        if not self.fast_models and not self.original_model:
            raise ValueError("No price prediction models are loaded")
        
        if self.fast_models:
            return self._predict_with_fast_models(product_data)
        else:
            return self._predict_with_original_model(product_data)
    
    def _predict_with_fast_models(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict using the fast multi-model system."""
        product_type = ProductClassifier.classify_product_type(product_data)
        
        if product_type not in self.fast_models['models']:
            raise ValueError(f"No model available for product type: {product_type}")
        
        # Extract enhanced features
        enhanced_features = self._extract_enhanced_features(
            product_data, 
            self.fast_models['brand_prestige_scores']
        )
        
        # Combine features
        combined_features = {**product_data, **enhanced_features}
        df = pd.DataFrame([combined_features])
        
        # Predict
        model_pipeline = self.fast_models['models'][product_type]
        pred_log = model_pipeline.predict(df)[0]
        price = float(np.expm1(pred_log))
        
        # Apply constraints
        constraints = settings.PRICE_CONSTRAINTS.get(product_type, (50, 10000))
        min_price, max_price = constraints
        price = max(min_price, min(price, max_price))
        
        return {
            "predicted_price": round(price, 2),
            "product_type": product_type,
            "model_type": "fast_multi_model"
        }
    
    def _predict_with_original_model(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict using the original single model."""
        df = pd.DataFrame([product_data])
        pred_log = self.original_model.predict(df)[0]
        price = float(np.expm1(pred_log))
        
        return {
            "predicted_price": round(price, 2),
            "model_type": "original_single_model"
        }
    
    def _extract_enhanced_features(self, product_data: Dict[str, Any], brand_prestige_scores: Dict[str, float]) -> Dict[str, Any]:
        """Extract enhanced features for the multi-model system."""
        product_name = str(product_data.get('product_name', ''))
        
        features = {
            'has_size': bool(re.search(r'\b(?:xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', product_name, re.IGNORECASE)),
            'name_length': len(product_name),
            'word_count': len(product_name.split()),
            'has_discount': float(product_data.get('discount_percent', 0)) > 0,
            'rating_count': int(product_data.get('rating_count', 0)),
            'discount_percent': float(product_data.get('discount_percent', 0)),
            'brand_avg_price': brand_prestige_scores.get(product_data.get('brand', '').lower(), 0)
        }
        
        # Material keywords
        materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather', 'cashmere', 'pashmina', 
                    'georgette', 'velvet', 'linen', 'chiffon', 'organza', 'net', 'lace']
        for material in materials:
            features[f'has_{material}'] = material.lower() in product_name.lower()
        
        # Style keywords
        styles = ['casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 'traditional',
                 'vintage', 'retro', 'modern', 'classic', 'trendy', 'elegant', 'chic']
        for style in styles:
            features[f'has_{style}'] = style.lower() in product_name.lower()
        
        # Jewelry-specific features
        jewelry_materials = ['gold', 'silver', 'platinum', 'diamond', 'gem', 'stone', 'pearl', 'crystal']
        for material in jewelry_materials:
            features[f'jewelry_{material}'] = material.lower() in product_name.lower()
        
        karat_match = re.search(r'(\d+)\s*kt', product_name, re.IGNORECASE)
        features['karat'] = float(karat_match.group(1)) if karat_match else 0.0
        
        # Watch-specific features
        watch_features = ['automatic', 'quartz', 'chronograph', 'digital', 'analog', 'waterproof', 'water resistant']
        for feature in watch_features:
            features[f'watch_{feature}'] = feature.lower() in product_name.lower()
        
        # Brand prestige
        brand = product_data.get('brand', '').lower()
        avg_price = brand_prestige_scores.get(brand, 0)
        if avg_price >= 5000:
            features['brand_prestige'] = 'ultra_premium'
        elif avg_price >= 2000:
            features['brand_prestige'] = 'premium'
        elif avg_price >= 500:
            features['brand_prestige'] = 'mid_range'
        else:
            features['brand_prestige'] = 'budget'
        
        # Luxury keywords
        luxury_keywords = ['designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
                          'embroidered', 'sequined', 'beaded', 'crystal', 'swarovski']
        for keyword in luxury_keywords:
            features[f'luxury_{keyword}'] = keyword.lower() in product_name.lower()
        
        features['price_range'] = 'medium'  # Default
        
        return features
    
    def get_recommendations(self, query: str, k: int = 10) -> Dict[str, Any]:
        """Get product recommendations based on query."""
        if not self.rec_collection or not self.embedding_model:
            raise ValueError("Recommendation system is not available")
        
        try:
            # Check if collection is empty
            if self.rec_collection.count() == 0:
                return {"results": []}
            
            # Generate embedding for query
            query_embedding = self.embedding_model.encode(query, normalize_embeddings=True).tolist()
            
            # Query ChromaDB
            res = self.rec_collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            results = []
            if res and res['ids'][0]:
                for i in range(len(res['ids'][0])):
                    results.append({
                        'id': res['ids'][0][i],
                        'document': res['documents'][0][i],
                        'metadata': res['metadatas'][0][i],
                        'distance': res['distances'][0][i] if res['distances'] else None
                    })
            
            return {"results": results}
            
        except Exception as e:
            raise ValueError(f"Recommendation query failed: {str(e)}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all models."""
        recs_loaded = self.rec_collection is not None
        try:
            recs_count = self.rec_collection.count() if self.rec_collection else 0
        except Exception:
            recs_count = 0
        
        return {
            "fast_models_loaded": self.fast_models is not None,
            "original_model_loaded": self.original_model is not None,
            "recs_index_loaded": recs_loaded,
            "recs_count": recs_count,
            "embedding_model_loaded": self.embedding_model is not None,
            "model_type_in_use": "fast_multi_model" if self.fast_models else "original_single_model"
        }
