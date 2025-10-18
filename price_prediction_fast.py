import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib
import re
import torch
import gc
from typing import Dict, List, Tuple, Any

class FastPricePredictor:
    """
    Fast price prediction system with specialized models for different product types
    Uses pre-tuned parameters for speed
    """
    
    def __init__(self):
        self.models = {}
        self.preprocessors = {}
        self.brand_prestige_scores = {}
        
    def check_gpu_availability(self):
        """Check if GPU is available and print GPU info"""
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(current_device)
            gpu_memory = torch.cuda.get_device_properties(current_device).total_memory / 1024**3
            print(f"✅ GPU Available: {gpu_name}")
            print(f"   GPU Memory: {gpu_memory:.1f} GB")
            print(f"   Device Count: {gpu_count}")
            return True
        else:
            print("❌ GPU not available, falling back to CPU")
            return False

    def clear_gpu_memory(self):
        """Clear GPU memory cache"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()

    def classify_product_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classify products into different types based on category and keywords"""
        df = df.copy()
        
        # Define product type classification rules
        jewelry_keywords = ['ring', 'chain', 'earring', 'necklace', 'bracelet', 'pendant', 'bangle', 
                           'diamond', 'gold', 'silver', 'platinum', 'karat', 'kt', 'gem', 'stone']
        
        watch_keywords = ['watch', 'chronograph', 'automatic', 'quartz', 'movement', 'dial', 'strap',
                         'timepiece', 'wristwatch', 'casio', 'titan', 'fastrack', 'fossil']
        
        luxury_keywords = ['designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
                          'cashmere', 'silk', 'leather', 'wool', 'pashmina', 'georgette', 'velvet']
        
        # Classify based on category and keywords
        def get_product_type(row):
            category = str(row.get('category', '')).lower()
            product_name = str(row.get('product_name', '')).lower()
            
            # Check for jewelry
            if any(keyword in category or keyword in product_name for keyword in jewelry_keywords):
                return 'jewelry'
            
            # Check for watches
            if any(keyword in category or keyword in product_name for keyword in watch_keywords):
                return 'watches'
            
            # Check for luxury items
            if any(keyword in product_name for keyword in luxury_keywords):
                return 'luxury_apparel'
            
            # Default to regular apparel
            return 'apparel'
        
        df['product_type'] = df.apply(get_product_type, axis=1)
        return df

    def extract_enhanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract enhanced features specific to different product types"""
        df = df.copy()
        
        # Basic features
        df['has_size'] = df['product_name'].str.contains(r'\b(?:xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', case=False, na=False)
        
        # Material keywords (expanded)
        materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather', 'cashmere', 'pashmina', 
                    'georgette', 'velvet', 'linen', 'chiffon', 'organza', 'net', 'lace']
        for material in materials:
            df[f'has_{material}'] = df['product_name'].str.contains(material, case=False, na=False)
        
        # Style keywords (expanded)
        styles = ['casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 'traditional',
                 'vintage', 'retro', 'modern', 'classic', 'trendy', 'elegant', 'chic']
        for style in styles:
            df[f'has_{style}'] = df['product_name'].str.contains(style, case=False, na=False)
        
        # Jewelry-specific features
        jewelry_materials = ['gold', 'silver', 'platinum', 'diamond', 'gem', 'stone', 'pearl', 'crystal']
        for material in jewelry_materials:
            df[f'jewelry_{material}'] = df['product_name'].str.contains(material, case=False, na=False)
        
        # Extract karat information
        df['karat'] = df['product_name'].str.extract(r'(\d+)\s*kt', flags=re.IGNORECASE).astype(float)
        df['karat'] = df['karat'].fillna(0)
        
        # Watch-specific features
        watch_features = ['automatic', 'quartz', 'chronograph', 'digital', 'analog', 'waterproof', 'water resistant']
        for feature in watch_features:
            df[f'watch_{feature}'] = df['product_name'].str.contains(feature, case=False, na=False)
        
        # Brand prestige scoring (based on average prices)
        brand_avg_prices = df.groupby('brand')['original_price'].mean().sort_values(ascending=False)
        self.brand_prestige_scores = brand_avg_prices.to_dict()
        
        # Create brand prestige tiers
        q25, q50, q75 = brand_avg_prices.quantile([0.25, 0.5, 0.75])
        
        def get_brand_prestige(brand):
            avg_price = self.brand_prestige_scores.get(brand, 0)
            if avg_price >= q75:
                return 'ultra_premium'
            elif avg_price >= q50:
                return 'premium'
            elif avg_price >= q25:
                return 'mid_range'
            else:
                return 'budget'
        
        df['brand_prestige'] = df['brand'].apply(get_brand_prestige)
        df['brand_avg_price'] = df['brand'].map(self.brand_prestige_scores).fillna(0)
        
        # Luxury keywords
        luxury_keywords = ['designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade',
                          'embroidered', 'sequined', 'beaded', 'crystal', 'swarovski']
        for keyword in luxury_keywords:
            df[f'luxury_{keyword}'] = df['product_name'].str.contains(keyword, case=False, na=False)
        
        # Product name features
        df['name_length'] = df['product_name'].str.len()
        df['word_count'] = df['product_name'].str.split().str.len()
        df['has_discount'] = (df['discount_percent'] > 0).astype(int)
        
        # Price range indicators
        df['price_range'] = pd.cut(df['original_price'], 
                                 bins=[0, 500, 1000, 2000, 5000, 20000, float('inf')],
                                 labels=['very_low', 'low', 'medium', 'high', 'very_high', 'ultra_high'])
        
        return df

    def get_features_for_product_type(self, product_type: str) -> Tuple[List[str], List[str]]:
        """Get appropriate features for each product type"""
        base_categorical = ['brand', 'gender', 'fabric', 'pattern', 'color', 'brand_prestige']
        base_numerical = ['rating_count', 'discount_percent', 'name_length', 'word_count', 'has_discount', 'brand_avg_price']
        
        if product_type == 'jewelry':
            categorical = base_categorical + ['price_range']
            numerical = base_numerical + ['karat'] + [f'jewelry_{mat}' for mat in ['gold', 'silver', 'platinum', 'diamond', 'gem', 'stone']]
            
        elif product_type == 'watches':
            categorical = base_categorical + ['price_range']
            numerical = base_numerical + [f'watch_{feat}' for feat in ['automatic', 'quartz', 'chronograph', 'digital', 'analog']]
            
        elif product_type == 'luxury_apparel':
            categorical = base_categorical + ['price_range']
            numerical = base_numerical + [f'luxury_{kw}' for kw in ['designer', 'couture', 'premium', 'exclusive', 'limited', 'handmade']]
            
        else:  # regular apparel
            categorical = base_categorical
            numerical = base_numerical + [f'has_{mat}' for mat in ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather', 'cashmere']]
        
        return categorical, numerical

    def get_optimized_params(self, product_type: str, gpu_available: bool = False) -> Dict:
        """Get pre-optimized parameters for each product type"""
        base_config = {
            'tree_method': 'gpu_hist' if gpu_available else 'hist',
            'device': 'cuda' if gpu_available else 'cpu',
            'random_state': 42,
            'verbosity': 0,
            'max_bin': 512,
            'grow_policy': 'lossguide',
            'max_leaves': 0,
            'sampling_method': 'gradient_based' if gpu_available else 'uniform'
        }
        
        if product_type == 'jewelry':
            return {
                **base_config,
                'n_estimators': 400,
                'max_depth': 8,
                'learning_rate': 0.05,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'reg_alpha': 0.1,
                'reg_lambda': 1.5
            }
        elif product_type == 'watches':
            return {
                **base_config,
                'n_estimators': 350,
                'max_depth': 7,
                'learning_rate': 0.08,
                'subsample': 0.85,
                'colsample_bytree': 0.85,
                'reg_alpha': 0.05,
                'reg_lambda': 1.2
            }
        elif product_type == 'luxury_apparel':
            return {
                **base_config,
                'n_estimators': 300,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.9,
                'colsample_bytree': 0.9,
                'reg_alpha': 0,
                'reg_lambda': 1
            }
        else:  # regular apparel
            return {
                **base_config,
                'n_estimators': 300,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.9,
                'colsample_bytree': 0.9,
                'reg_alpha': 0,
                'reg_lambda': 1
            }

    def train_specialized_model(self, df: pd.DataFrame, product_type: str, gpu_available: bool = False):
        """Train a specialized model for a specific product type with pre-optimized parameters"""
        print(f"\n🚀 Training FAST model for {product_type}...")
        
        # Filter data for this product type
        df_type = df[df['product_type'] == product_type].copy()
        
        if len(df_type) < 1000:
            print(f"⚠️  Insufficient data for {product_type} ({len(df_type)} samples), skipping...")
            return None
        
        print(f"   Dataset size: {len(df_type):,} samples")
        
        # Get appropriate features
        categorical_features, numerical_features = self.get_features_for_product_type(product_type)
        
        # Prepare data
        X = df_type[categorical_features + numerical_features]
        y = np.log1p(df_type['original_price'])
        
        # Use smaller sample for faster training
        if len(df_type) > 30_000:
            print(f"   Using 30k sample for fast training...")
            df_sample = df_type.sample(30_000, random_state=42)
            X_sample = df_sample[categorical_features + numerical_features]
            y_sample = np.log1p(df_sample['original_price'])
        else:
            X_sample = X
            y_sample = y
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42)
        
        # Preprocessing
        preprocessor = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', min_frequency=5), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ])
        
        # Get optimized parameters
        xgb_params = self.get_optimized_params(product_type, gpu_available)
        
        # Create pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', XGBRegressor(**xgb_params))
        ])
        
        print(f"   Training with pre-optimized parameters (no grid search)...")
        
        # Clear memory before training
        self.clear_gpu_memory()
        
        # Train directly without grid search
        pipeline.fit(X_train, y_train)
        
        # Clear memory after training
        self.clear_gpu_memory()
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        y_true_orig = np.expm1(y_test)
        y_pred_orig = np.expm1(y_pred)
        
        rmse = np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))
        mae = mean_absolute_error(y_true_orig, y_pred_orig)
        r2 = r2_score(y_true_orig, y_pred_orig)
        
        print(f"   {product_type} Model Performance:")
        print(f"   RMSE: ₹{int(rmse)}, MAE: ₹{int(mae)}, R²: {r2:.4f}")
        
        # Store model and features
        self.models[product_type] = pipeline
        self.preprocessors[product_type] = {
            'categorical_features': categorical_features,
            'numerical_features': numerical_features,
            'feature_names': categorical_features + numerical_features
        }
        
        return pipeline

    def apply_price_constraints(self, predictions: np.ndarray, product_type: str) -> np.ndarray:
        """Apply price constraints based on product type"""
        constraints = {
            'jewelry': (100, 200000),      # ₹100 to ₹2L
            'watches': (500, 100000),      # ₹500 to ₹1L
            'luxury_apparel': (1000, 50000), # ₹1K to ₹50K
            'apparel': (50, 10000)         # ₹50 to ₹10K
        }
        
        min_price, max_price = constraints.get(product_type, (50, 10000))
        predictions = np.clip(predictions, min_price, max_price)
        return predictions

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the appropriate specialized model"""
        predictions = np.zeros(len(X))
        
        for product_type in self.models.keys():
            mask = X['product_type'] == product_type
            if mask.sum() == 0:
                continue
                
            X_type = X[mask]
            categorical_features = self.preprocessors[product_type]['categorical_features']
            numerical_features = self.preprocessors[product_type]['numerical_features']
            
            X_features = X_type[categorical_features + numerical_features]
            pred_log = self.models[product_type].predict(X_features)
            pred_orig = np.expm1(pred_log)
            
            # Apply price constraints
            pred_orig = self.apply_price_constraints(pred_orig, product_type)
            
            predictions[mask] = pred_orig
        
        return predictions

    def save_models(self, save_dir: str = 'artifacts'):
        """Save all trained models and metadata"""
        os.makedirs(save_dir, exist_ok=True)
        
        model_data = {
            'models': self.models,
            'preprocessors': self.preprocessors,
            'brand_prestige_scores': self.brand_prestige_scores,
            'product_classifier': self.classify_product_type
        }
        
        model_path = os.path.join(save_dir, 'fast_price_models.joblib')
        joblib.dump(model_data, model_path)
        print(f"💾 Saved fast models to {model_path}")

def main():
    """Main training function - FAST VERSION"""
    print("⚡ Starting FAST Multi-Model Price Prediction Training...")
    print("   (No grid search - using pre-optimized parameters)")
    
    # Initialize predictor
    predictor = FastPricePredictor()
    
    # Check GPU availability
    gpu_available = predictor.check_gpu_availability()
    predictor.clear_gpu_memory()
    
    # Load and prepare data
    print("\n📊 Loading and preparing data...")
    df = pd.read_parquet('myntra_cleaned.parquet')
    df = df[(df['original_price'] > 0) & (df['discounted_price'] > 0)]
    
    # Classify product types
    print("🔍 Classifying product types...")
    df = predictor.classify_product_type(df)
    
    # Show product type distribution
    type_counts = df['product_type'].value_counts()
    print(f"\nProduct Type Distribution:")
    for ptype, count in type_counts.items():
        print(f"  {ptype}: {count:,} items ({count/len(df)*100:.1f}%)")
    
    # Extract enhanced features
    print("\n✨ Extracting enhanced features...")
    df = predictor.extract_enhanced_features(df)
    
    # Train specialized models
    print("\n🎯 Training specialized models (FAST MODE)...")
    for product_type in df['product_type'].unique():
        predictor.train_specialized_model(df, product_type, gpu_available)
    
    # Save models
    predictor.save_models()
    
    print("\n✅ FAST multi-model training completed!")


if __name__ == "__main__":
    main()
