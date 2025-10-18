from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import joblib
import pandas as pd
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: chromadb or sentence-transformers not available, recommendation system disabled")
import numpy as np
import re
from typing import Dict, List, Any

# --- App Initialization ---
app = FastAPI(title="Fashion GenAI API", version="1.0.0")

# --- Global Variables ---
fast_models = None
original_model = None
rec_collection = None
embedding_model = None

# --- Startup Event: Load Models ---
@app.on_event("startup")
def load_models():
    """Load all ML models and databases when the API starts."""
    global fast_models, original_model, rec_collection, embedding_model

    print("Starting model loading process...")
    
    # Check if artifacts directory exists
    if not os.path.exists('artifacts'):
        print("Artifacts directory not found, creating...")
        os.makedirs('artifacts', exist_ok=True)

    # Load fast multi-model system for price prediction
    FAST_MODEL_PATH = os.path.join('artifacts', 'fast_price_models_api.joblib')
    print(f"Looking for fast models at: {FAST_MODEL_PATH}")
    
    if os.path.exists(FAST_MODEL_PATH):
        try:
            fast_models = joblib.load(FAST_MODEL_PATH)
            print("Fast multi-model system loaded successfully")
        except Exception as e:
            print(f"Could not load fast models: {e}")
    else:
        print(f"Fast model file not found at {FAST_MODEL_PATH}")

    # Fallback to original single model if fast models not available
    ORIGINAL_MODEL_PATH = os.path.join('artifacts', 'price_model_improved.joblib')
    print(f"Looking for original model at: {ORIGINAL_MODEL_PATH}")
    
    if not fast_models and os.path.exists(ORIGINAL_MODEL_PATH):
        try:
            original_model = joblib.load(ORIGINAL_MODEL_PATH)['pipeline']
            print("Original model loaded as fallback")
        except Exception as e:
            print(f"Could not load original model: {e}")
    else:
        print(f"Original model file not found at {ORIGINAL_MODEL_PATH}")
    
    # Final fallback to lightweight model
    FALLBACK_MODEL_PATH = os.path.join('artifacts', 'fallback_model.joblib')
    print(f"Looking for fallback model at: {FALLBACK_MODEL_PATH}")
    
    if not fast_models and not original_model and os.path.exists(FALLBACK_MODEL_PATH):
        try:
            original_model = joblib.load(FALLBACK_MODEL_PATH)['pipeline']
            print("Fallback model loaded successfully")
        except Exception as e:
            print(f"Could not load fallback model: {e}")
    else:
        print(f"Fallback model file not found at {FALLBACK_MODEL_PATH}")
    
    # Create a simple model on startup if no models are available
    if not fast_models and not original_model:
        print("Creating simple fallback model on startup...")
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.preprocessing import StandardScaler, OneHotEncoder
            from sklearn.compose import ColumnTransformer
            from sklearn.pipeline import Pipeline
            import pandas as pd
            import numpy as np
            
            # Create a simple synthetic dataset
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
            
            # Create simple model
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
            
            # Train the model
            model.fit(X, y)
            original_model = model
            print("Simple fallback model created and loaded successfully")
            
        except Exception as e:
            print(f"Could not create fallback model: {e}")
    
    # List all files in artifacts directory for debugging
    if os.path.exists('artifacts'):
        print("Files in artifacts directory:")
        for file in os.listdir('artifacts'):
            file_path = os.path.join('artifacts', file)
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
            print(f"  - {file} ({size} bytes)")
    
    if not fast_models and not original_model:
        print("WARNING: No price prediction models loaded!")

    # Load ChromaDB and Sentence Transformer for recommendations
    if CHROMADB_AVAILABLE:
        try:
            # Load the embedding model
            embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("SentenceTransformer embedding model loaded")
            
            # Connect to the persistent ChromaDB client
            chroma_client = chromadb.PersistentClient(path="./chroma_db")
            collection_name = 'fashion'
            rec_collection = chroma_client.get_collection(collection_name)
            try:
                rec_count = rec_collection.count()
            except Exception:
                rec_count = 0
            print(f"ChromaDB collection '{collection_name}' loaded successfully (items: {rec_count})")
        except Exception as e:
            print(f"ChromaDB or embedding model could not be loaded: {e}")
            rec_collection = None
            embedding_model = None

# --- Pydantic Models for Request Validation ---
class PriceRequest(BaseModel):
    product_name: str
    brand: str
    gender: str
    category: str
    fabric: str | None = None
    pattern: str | None = None
    color: str | None = None
    rating_count: int = 0
    discount_percent: float = 0.0

class SearchRequest(BaseModel):
    query: str
    k: int = 10

# --- Helper Functions for Price Prediction ---
def classify_product_type(row: Dict) -> str:
    """Classify products into different types based on category and keywords."""
    jewelry_keywords = ['ring', 'chain', 'earring', 'necklace', 'bracelet', 'pendant', 'bangle', 
                       'diamond', 'gold', 'silver', 'platinum', 'karat', 'kt', 'gem', 'stone']
    
    watch_keywords = ['watch', 'chronograph', 'automatic', 'quartz', 'movement', 'dial', 'strap',
                     'timepiece', 'wristwatch', 'casio', 'titan', 'fastrack', 'fossil']
    
    luxury_keywords = ['designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
                      'cashmere', 'silk', 'leather', 'wool', 'pashmina', 'georgette', 'velvet']
    
    category = str(row.get('category', '')).lower()
    product_name = str(row.get('product_name', '')).lower()
    
    if any(keyword in category or keyword in product_name for keyword in jewelry_keywords):
        return 'jewelry'
    elif any(keyword in category or keyword in product_name for keyword in watch_keywords):
        return 'watches'
    elif any(keyword in product_name for keyword in luxury_keywords):
        return 'luxury_apparel'
    else:
        return 'apparel'

def extract_enhanced_features(row: Dict, brand_prestige_scores: Dict) -> Dict:
    """Extract enhanced features for the multi-model system."""
    product_name = str(row.get('product_name', ''))
    
    features = {
        'has_size': bool(re.search(r'\b(?:xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', product_name, re.IGNORECASE)),
        'name_length': len(product_name),
        'word_count': len(product_name.split()),
        'has_discount': float(row.get('discount_percent', 0)) > 0,
        'rating_count': int(row.get('rating_count', 0)),
        'discount_percent': float(row.get('discount_percent', 0)),
        'brand_avg_price': brand_prestige_scores.get(row.get('brand', '').lower(), 0)
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
    brand = row.get('brand', '').lower()
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

# --- API Endpoints ---
@app.get("/healthz")
def healthz():
    """Health check endpoint to verify model and DB status."""
    recs_loaded = rec_collection is not None
    try:
        recs_count = rec_collection.count() if rec_collection else 0
    except Exception:
        recs_count = 0
    return {
        "status": "ok", 
        "fast_models_loaded": fast_models is not None, 
        "original_model_loaded": original_model is not None,
        "recs_index_loaded": recs_loaded,
        "recs_count": recs_count,
        "embedding_model_loaded": embedding_model is not None,
        "model_type_in_use": "fast_multi_model" if fast_models else "original_single_model"
    }

@app.post("/predict_price")
def predict_price(req: PriceRequest):
    """Predicts the price of a fashion item using the best available model."""
    if fast_models is None and original_model is None:
        raise HTTPException(status_code=503, detail="No price models are loaded.")
    
    input_data = req.dict()
    
    if fast_models:
        try:
            product_type = classify_product_type(input_data)
            
            if product_type in fast_models['models']:
                # *** FIX STARTS HERE ***
                # 1. Combine original input with newly extracted features
                enhanced_features = extract_enhanced_features(input_data, fast_models['brand_prestige_scores'])
                combined_features = {**input_data, **enhanced_features}
                
                # 2. Create a DataFrame from the combined dictionary
                df = pd.DataFrame([combined_features])
                
                # 3. Get the correct model for the product type
                model_pipeline = fast_models['models'][product_type]
                
                # 4. Predict using the full pipeline (which includes preprocessing)
                pred_log = model_pipeline.predict(df)[0]
                price = float(np.expm1(pred_log))
                # *** FIX ENDS HERE ***
                
                # Apply price constraints
                constraints = {'jewelry': (100, 200000), 'watches': (500, 100000), 'luxury_apparel': (1000, 50000), 'apparel': (50, 10000)}
                min_price, max_price = constraints.get(product_type, (50, 10000))
                price = max(min_price, min(price, max_price))
                
                return {"predicted_price": round(price, 2), "product_type": product_type, "model_type": "fast_multi_model"}
            else:
                raise HTTPException(status_code=404, detail=f"No model available for product type: {product_type}")
        except Exception as e:
            # Propagate the actual error for better debugging
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Fallback to original model
    else:
        df = pd.DataFrame([input_data])
        pred_log = original_model.predict(df)[0]
        price = float(np.expm1(pred_log))
        return {"predicted_price": round(price, 2), "model_type": "original_single_model"}

@app.post("/recommend_products")
def recommend_products(req: SearchRequest):
    """Recommends similar fashion items based on a text query."""
    if rec_collection is None or embedding_model is None:
        raise HTTPException(status_code=503, detail="Recommendation system is not available.")
    
    try:
        # Skip querying if index is empty
        try:
            if rec_collection.count() == 0:
                return {"results": []}
        except Exception:
            pass
        # Generate embedding for the user's query
        query_embedding = embedding_model.encode(req.query, normalize_embeddings=True).tolist()
        
        # Query ChromaDB to find similar items
        res = rec_collection.query(
            query_embeddings=[query_embedding], 
            n_results=req.k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format the results
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
        raise HTTPException(status_code=500, detail=f"Recommendation query failed: {str(e)}")

