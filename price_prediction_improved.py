import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import joblib
import re

def extract_features(df):
    """Extract additional features from product names"""
    df = df.copy()
    
    # Extract size information
    df['has_size'] = df['product_name'].str.contains(r'\b(xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', case=False, na=False)
    
    # Extract material keywords
    materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather', 'canvas', 'linen', 'viscose', 'rayon']
    for material in materials:
        df[f'has_{material}'] = df['product_name'].str.contains(material, case=False, na=False)
    
    # Extract style keywords
    styles = ['casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 'traditional']
    for style in styles:
        df[f'has_{style}'] = df['product_name'].str.contains(style, case=False, na=False)
    
    # Extract brand tier (expanded for better high-price prediction)
    premium_brands = ['gucci', 'prada', 'versace', 'armani', 'louis vuitton', 'chanel', 'dior', 'hermes', 'balenciaga', 'givenchy', 'ysl', 'saint laurent']
    mid_brands = ['zara', 'h&m', 'uniqlo', 'mango', 'massimo dutti', 'cos', 'everlane', 'reformation']
    luxury_brands = ['rolex', 'omega', 'cartier', 'tiffany', 'bulgari', 'montblanc']
    
    df['brand_tier'] = 'budget'
    df.loc[df['brand'].isin(mid_brands), 'brand_tier'] = 'mid'
    df.loc[df['brand'].isin(premium_brands), 'brand_tier'] = 'premium'
    df.loc[df['brand'].isin(luxury_brands), 'brand_tier'] = 'luxury'
    
    # High-value keywords for expensive items
    luxury_keywords = luxury_keywords = ['cashmere', 'embroidered', 'handmade', 'limited', 'exclusive', 'premium', 'designer', 'couture', 'vintage', 'antique']
    for keyword in luxury_keywords:
        df[f'has_{keyword}'] = df['product_name'].str.contains(keyword, case=False, na=False)
    
    # Product name length (proxy for description richness)
    df['name_length'] = df['product_name'].str.len()
    
    # Has discount flag
    df['has_discount'] = (df['discount_percent'] > 0).astype(int)
    
    return df

# Load and prepare data
print("Loading data...")
df = pd.read_parquet('myntra_cleaned.parquet')
df = df[(df['original_price'] > 0) & (df['discounted_price'] > 0)]

print("Extracting features...")
df = extract_features(df)

# Feature selection
categorical_features = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color', 'brand_tier']
numerical_features = ['rating_count', 'discount_percent', 'name_length', 'has_discount'] + \
                    [f'has_{mat}' for mat in ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather']] + \
                    [f'has_{style}' for style in ['casual', 'formal', 'sport', 'ethnic', 'western']] + \
                   [f'has_{keyword}' for keyword in ['cashmere', 'embroidered', 'handmade', 'limited', 'exclusive', 'premium', 'designer', 'couture', 'vintage', 'antique']]
X = df[categorical_features + numerical_features]
y = np.log1p(df['original_price'])  # Log transform for better performance

print(f"Features: {len(categorical_features)} categorical, {len(numerical_features)} numerical")
print(f"Dataset size: {len(df):,} samples")

# Preprocessing
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', min_frequency=50), categorical_features),
    ('num', StandardScaler(), numerical_features)
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Try multiple models
models = {
    'XGBoost_GPU': XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        tree_method='hist',
        device='cuda',
        random_state=42,
        verbosity=0
    ),
    'XGBoost_CPU': XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        verbosity=0
    ),
    'LightGBM': LGBMRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        num_leaves=31,
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )
}

best_model = None
best_score = float('inf')
best_name = ""

for name, model in models.items():
    print(f"\nTraining {name}...")
    
    # Create pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Convert back to original scale for interpretation
    y_true_orig = np.expm1(y_test)
    y_pred_orig = np.expm1(y_pred)
    rmse_orig = np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))
    
    print(f"  RMSE (log scale): {rmse:.4f}")
    print(f"  RMSE (original): ₹{int(rmse_orig)}")
    print(f"  MAE (original): ₹{int(mean_absolute_error(y_true_orig, y_pred_orig))}")
    print(f"  R²: {r2:.4f}")
    
    if rmse_orig < best_score:
        best_score = rmse_orig
        best_model = pipeline
        best_name = name

print(f"\nBest model: {best_name} (RMSE: ₹{int(best_score)})")

# Save best model
os.makedirs('artifacts', exist_ok=True)
model_path = os.path.join('artifacts', 'price_model_improved.joblib')
joblib.dump({
    'pipeline': best_model,
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'feature_names': categorical_features + numerical_features
}, model_path)
print(f'Saved improved model to {model_path}')

# Feature importance (if available)
if hasattr(best_model.named_steps['model'], 'feature_importances_'):
    feature_names = best_model.named_steps['preprocessor'].get_feature_names_out()
    importances = best_model.named_steps['model'].feature_importances_
    
    # Get top 20 most important features
    top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 most important features:")
    for feature, importance in top_features:
        print(f"  {feature}: {importance:.4f}")
