import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib
import re
import torch
import gc

def check_gpu_availability():
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

def clear_gpu_memory():
    """Clear GPU memory cache"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

def get_gpu_memory_info():
    """Get current GPU memory usage"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        cached = torch.cuda.memory_reserved() / 1024**3
        return f"GPU Memory - Allocated: {allocated:.2f}GB, Cached: {cached:.2f}GB"
    return "GPU not available"

def extract_features(df):
    """Extract additional features from product names"""
    df = df.copy()
    
    # Extract size information
    df['has_size'] = df['product_name'].str.contains(r'\b(xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', case=False, na=False)
    
    # Extract material keywords
    materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather']
    for material in materials:
        df[f'has_{material}'] = df['product_name'].str.contains(material, case=False, na=False)
    
    # Extract style keywords
    styles = ['casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 'traditional']
    for style in styles:
        df[f'has_{style}'] = df['product_name'].str.contains(style, case=False, na=False)
    
    # Extract brand tier based on ACTUAL average prices in dataset
    brand_avg_prices = df.groupby('brand')['original_price'].mean().sort_values(ascending=False)
    q33, q67 = brand_avg_prices.quantile([0.33, 0.67])
    
    def get_brand_tier(brand):
        avg_price = brand_avg_prices.get(brand, 0)
        if avg_price >= q67:
            return 'premium'
        elif avg_price >= q33:
            return 'mid'
        else:
            return 'budget'
    
    df['brand_tier'] = df['brand'].apply(get_brand_tier)
    
    # High-value keywords for expensive items
    luxury_keywords = ['leather', 'silk', 'cashmere', 'wool', 'embroidered', 'handmade', 'limited', 'exclusive', 'premium', 'designer', 'couture', 'vintage', 'antique']
    for keyword in luxury_keywords:
        df[f'has_{keyword}'] = df['product_name'].str.contains(keyword, case=False, na=False)
    
    # Product name length (proxy for description richness)
    df['name_length'] = df['product_name'].str.len()
    
    # Has discount flag
    df['has_discount'] = (df['discount_percent'] > 0).astype(int)
    
    return df

# Check GPU availability
gpu_available = check_gpu_availability()
clear_gpu_memory()

# Load and prepare data
print("Loading data...")
df = pd.read_parquet('myntra_cleaned.parquet')
df = df[(df['original_price'] > 0) & (df['discounted_price'] > 0)]

print("Extracting features...")
df = extract_features(df)

# Feature selection
categorical_features = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color', 'brand_tier']
materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather']
styles = ['casual', 'formal', 'sport', 'ethnic', 'western']
luxury_keywords = ['leather', 'silk', 'cashmere', 'wool', 'embroidered', 'handmade', 'limited', 'exclusive', 'premium', 'designer', 'couture', 'vintage', 'antique']

all_keywords = list(set(materials + styles + luxury_keywords))
numerical_features = ['rating_count', 'discount_percent', 'name_length', 'has_discount'] + \
                    [f'has_{keyword}' for keyword in all_keywords]

X = df[categorical_features + numerical_features]
y = np.log1p(df['original_price'])

print(f"Features: {len(categorical_features)} categorical, {len(numerical_features)} numerical")
print(f"Dataset size: {len(df):,} samples")

# Use smaller sample for hyperparameter tuning (faster)
print("Using 200k sample for hyperparameter tuning...")
df_sample = df.sample(200_000, random_state=42)
X_sample = df_sample[categorical_features + numerical_features]
y_sample = np.log1p(df_sample['original_price'])

# Preprocessing
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', min_frequency=20), categorical_features),
    ('num', StandardScaler(), numerical_features)
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42)

# Hyperparameter grid for XGBoost
xgb_params = {
    'model__n_estimators': [300, 500],
    'model__max_depth': [6, 8, 10],
    'model__learning_rate': [0.05, 0.1, 0.15],
    'model__subsample': [0.8, 0.9, 1.0],
    'model__colsample_bytree': [0.8, 0.9, 1.0],
    'model__reg_alpha': [0, 0.1, 0.5],
    'model__reg_lambda': [1, 1.5, 2]
}

print("Starting hyperparameter tuning...")

# Configure XGBoost for optimal GPU usage
xgb_config = {
    'tree_method': 'gpu_hist' if gpu_available else 'hist',
    'device': 'cuda' if gpu_available else 'cpu',
    'random_state': 42,
    'verbosity': 0,
    'gpu_id': 0 if gpu_available else None,
    'max_bin': 512,  # Optimize for GPU memory
    'grow_policy': 'lossguide',  # Better for GPU
    'max_leaves': 0,  # Let GPU decide
    'sampling_method': 'gradient_based' if gpu_available else 'uniform'
}

xgb_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', XGBRegressor(**xgb_config))
])

# Grid search with 3-fold CV
print(f"GridSearch configuration:")
print(f"  - GPU enabled: {gpu_available}")
print(f"  - Tree method: {'gpu_hist' if gpu_available else 'hist'}")
print(f"  - Device: {'cuda' if gpu_available else 'cpu'}")
print(f"  - Total combinations: {len(xgb_params['model__n_estimators']) * len(xgb_params['model__max_depth']) * len(xgb_params['model__learning_rate']) * len(xgb_params['model__subsample']) * len(xgb_params['model__colsample_bytree']) * len(xgb_params['model__reg_alpha']) * len(xgb_params['model__reg_lambda'])}")

grid_search = GridSearchCV(
    xgb_pipeline, 
    xgb_params, 
    cv=3, 
    scoring='neg_mean_squared_error',
    n_jobs=1,  # Use 1 job to avoid GPU conflicts
    verbose=2,  # More verbose output
    return_train_score=True
)

# Clear memory before starting
clear_gpu_memory()

print("\n🚀 Starting GridSearch with GPU acceleration...")
grid_search.fit(X_train, y_train)

# Clear memory after training
clear_gpu_memory()

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {-grid_search.best_score_:.4f}")
print(f"GPU Status: {get_gpu_memory_info()}")

# Evaluate on test set
y_pred = grid_search.predict(X_test)
y_true_orig = np.expm1(y_test)
y_pred_orig = np.expm1(y_pred)

rmse = np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))
mae = mean_absolute_error(y_true_orig, y_pred_orig)
r2 = r2_score(y_true_orig, y_pred_orig)

print(f"\nTuned Model Performance:")
print(f"RMSE: ₹{int(rmse)}")
print(f"MAE: ₹{int(mae)}")
print(f"R²: {r2:.4f}")

# Price quartile analysis
q25, q50, q75 = np.percentile(y_true_orig, [25, 50, 75])
low_mask = y_true_orig <= q25
mid_mask = (y_true_orig > q25) & (y_true_orig <= q75)
high_mask = y_true_orig > q75

print(f"\nPrice quartiles: Q1=₹{int(q25)}, Q2=₹{int(q50)}, Q3=₹{int(q75)}")
print(f"RMSE for low prices (≤₹{int(q25)}): ₹{int(np.sqrt(mean_squared_error(y_true_orig[low_mask], y_pred_orig[low_mask])))}")
print(f"RMSE for mid prices (₹{int(q25)}-₹{int(q75)}): ₹{int(np.sqrt(mean_squared_error(y_true_orig[mid_mask], y_pred_orig[mid_mask])))}")
print(f"RMSE for high prices (>₹{int(q75)}): ₹{int(np.sqrt(mean_squared_error(y_true_orig[high_mask], y_pred_orig[high_mask])))}")

# Save tuned model
os.makedirs('artifacts', exist_ok=True)
model_path = os.path.join('artifacts', 'price_model_tuned.joblib')
joblib.dump({
    'pipeline': grid_search.best_estimator_,
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'feature_names': categorical_features + numerical_features,
    'best_params': grid_search.best_params_
}, model_path)
print(f'Saved tuned model to {model_path}')

# Final memory cleanup
clear_gpu_memory()
print(f"Final GPU Status: {get_gpu_memory_info()}")

# Feature importance
if hasattr(grid_search.best_estimator_.named_steps['model'], 'feature_importances_'):
    feature_names = grid_search.best_estimator_.named_steps['preprocessor'].get_feature_names_out()
    importances = grid_search.best_estimator_.named_steps['model'].feature_importances_
    
    top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 most important features:")
    for feature, importance in top_features:
        print(f"  {feature}: {importance:.4f}")
