#!/usr/bin/env python3
"""
Create a simple fallback model for deployment when main models are too large.
This creates a lightweight model that can be deployed to Render.
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import os

def create_fallback_model():
    """Create a simple fallback model for deployment."""
    print("Creating fallback model for deployment...")
    
    # Create a simple synthetic dataset for training
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic data
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
    
    # Create a simple price based on features
    base_price = 1000
    brand_multiplier = {
        'nike': 1.5, 'adidas': 1.4, 'zara': 1.2, 'h&m': 1.0, 'roadster': 0.8
    }
    category_multiplier = {
        'shoes': 1.3, 'dress': 1.2, 'jeans': 1.1, 'shirt': 1.0
    }
    
    prices = []
    for _, row in df.iterrows():
        price = base_price
        price *= brand_multiplier.get(row['brand'], 1.0)
        price *= category_multiplier.get(row['category'], 1.0)
        price *= (1 - row['discount_percentage'] / 100)
        price += np.random.normal(0, 100)  # Add some noise
        prices.append(max(100, price))  # Minimum price of 100
    
    df['price'] = prices
    
    # Prepare features and target
    feature_columns = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color', 'number_of_ratings', 'discount_percentage']
    X = df[feature_columns]
    y = df['price']
    
    # Create preprocessing pipeline
    categorical_features = ['brand', 'gender', 'category', 'fabric', 'pattern', 'color']
    numerical_features = ['number_of_ratings', 'discount_percentage']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # Create model pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    
    # Train the model
    print("Training fallback model...")
    model.fit(X, y)
    
    # Create the model package
    model_package = {
        'pipeline': model,
        'feature_columns': feature_columns,
        'model_type': 'fallback'
    }
    
    # Save the model
    os.makedirs('artifacts', exist_ok=True)
    model_path = 'artifacts/fallback_model.joblib'
    joblib.dump(model_package, model_path)
    
    print(f"Fallback model saved to {model_path}")
    
    # Test the model
    test_data = pd.DataFrame([{
        'brand': 'roadster',
        'gender': 'men',
        'category': 'shirt',
        'fabric': 'cotton',
        'pattern': 'solid',
        'color': 'blue',
        'number_of_ratings': 500,
        'discount_percentage': 40
    }])
    
    prediction = model.predict(test_data)[0]
    print(f"Test prediction: Rs {prediction:.2f}")
    
    return model_path

if __name__ == "__main__":
    create_fallback_model()
