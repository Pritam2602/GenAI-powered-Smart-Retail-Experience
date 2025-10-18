#!/usr/bin/env python3
"""
Save models in a format that can be loaded by the API without class dependencies
"""

import joblib
import os
from price_prediction_fast import FastPricePredictor

def save_models_for_api():
    """Save models in API-compatible format"""
    print("Converting models for API compatibility...")
    
    # Load the fast models
    try:
        model_data = joblib.load('artifacts/fast_price_models.joblib')
        print("Loaded fast models")
    except Exception as e:
        print(f"Could not load fast models: {e}")
        return
    
    # Extract only the essential data (no class references)
    api_compatible_data = {
        'models': model_data['models'],
        'preprocessors': model_data['preprocessors'],
        'brand_prestige_scores': model_data['brand_prestige_scores']
    }
    
    # Save in API-compatible format
    api_model_path = 'artifacts/fast_price_models_api.joblib'
    joblib.dump(api_compatible_data, api_model_path)
    print(f"Saved API-compatible models to {api_model_path}")
    
    # Test loading
    try:
        test_load = joblib.load(api_model_path)
        print("API-compatible models can be loaded successfully")
        print(f"   Available models: {list(test_load['models'].keys())}")
    except Exception as e:
        print(f"Error testing API-compatible models: {e}")

if __name__ == "__main__":
    save_models_for_api()
