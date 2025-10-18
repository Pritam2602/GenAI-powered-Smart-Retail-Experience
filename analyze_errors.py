import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib

# Load the improved model
model_data = joblib.load('artifacts/price_model_improved.joblib')
pipeline = model_data['pipeline']
categorical_features = model_data['categorical_features']
numerical_features = model_data['numerical_features']

# Load and prepare data (same as training)
def extract_features(df):
    df = df.copy()
    df['has_size'] = df['product_name'].str.contains(r'\b(?:xs|s|m|l|xl|xxl|xxxl|small|medium|large)\b', case=False, na=False)
    
    materials = ['cotton', 'polyester', 'silk', 'wool', 'denim', 'leather']
    for material in materials:
        df[f'has_{material}'] = df['product_name'].str.contains(material, case=False, na=False)
    
    styles = ['casual', 'formal', 'sport', 'party', 'wedding', 'ethnic', 'western', 'traditional']
    for style in styles:
        df[f'has_{style}'] = df['product_name'].str.contains(style, case=False, na=False)
    
    # Brand tier based on actual prices
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
    
    luxury_keywords = ['leather', 'silk', 'cashmere', 'wool', 'embroidered', 'handmade', 'limited', 'exclusive', 'premium', 'designer', 'couture', 'vintage', 'antique']
    for keyword in luxury_keywords:
        df[f'has_{keyword}'] = df['product_name'].str.contains(keyword, case=False, na=False)
    
    df['name_length'] = df['product_name'].str.len()
    df['has_discount'] = (df['discount_percent'] > 0).astype(int)
    return df

print("Loading data for error analysis...")
df = pd.read_parquet('myntra_cleaned.parquet')
df = df[(df['original_price'] > 0) & (df['discounted_price'] > 0)]
df = extract_features(df)

X = df[categorical_features + numerical_features]
y = np.log1p(df['original_price'])

# Use a sample for analysis
df_sample = df.sample(50_000, random_state=42).reset_index(drop=True)
X_sample = df_sample[categorical_features + numerical_features]
y_sample = np.log1p(df_sample['original_price'])

print("Making predictions...")
y_pred_log = pipeline.predict(X_sample)
y_true_orig = np.expm1(y_sample)
y_pred_orig = np.expm1(y_pred_log)

# Calculate residuals
residuals = y_true_orig - y_pred_orig
abs_residuals = np.abs(residuals)

print(f"Residual Analysis:")
print(f"Mean residual: ₹{np.mean(residuals):.2f}")
print(f"Std residual: ₹{np.std(residuals):.2f}")
print(f"Max positive residual: ₹{np.max(residuals):.2f}")
print(f"Max negative residual: ₹{np.min(residuals):.2f}")

# Find worst predictions
worst_indices = np.argsort(abs_residuals)[-20:]
print(f"\nWorst 20 predictions:")
for i in worst_indices:
    actual = y_true_orig.iloc[i]
    predicted = y_pred_orig[i]
    error = abs_residuals[i]
    brand = df_sample.iloc[i]['brand']
    product = df_sample.iloc[i]['product_name'][:50]
    print(f"  Actual: ₹{actual:.0f}, Predicted: ₹{predicted:.0f}, Error: ₹{error:.0f}")
    print(f"    Brand: {brand}, Product: {product}...")
    print()

# Price range analysis
price_ranges = [
    (0, 500, "Very Low"),
    (500, 1000, "Low"), 
    (1000, 2000, "Medium"),
    (2000, 5000, "High"),
    (5000, float('inf'), "Very High")
]

print("Error analysis by price range:")
for min_price, max_price, label in price_ranges:
    mask = (y_true_orig >= min_price) & (y_true_orig < max_price)
    if mask.sum() > 0:
        range_residuals = residuals[mask]
        range_rmse = np.sqrt(np.mean(range_residuals**2))
        range_mae = np.mean(np.abs(range_residuals))
        count = mask.sum()
        print(f"  {label} (₹{min_price}-₹{max_price}): {count} items, RMSE: ₹{range_rmse:.0f}, MAE: ₹{range_mae:.0f}")

# Brand analysis for high errors
high_error_mask = abs_residuals > np.percentile(abs_residuals, 95)
high_error_brands = df_sample[high_error_mask]['brand'].value_counts().head(10)
print(f"\nBrands with highest errors (top 10):")
for brand, count in high_error_brands.items():
    print(f"  {brand}: {count} high-error items")

# Category analysis for high errors
high_error_categories = df_sample[high_error_mask]['category'].value_counts().head(10)
print(f"\nCategories with highest errors (top 10):")
for category, count in high_error_categories.items():
    print(f"  {category}: {count} high-error items")
