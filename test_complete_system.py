#!/usr/bin/env python3
"""
Test script for the complete Fast Multi-Model System with ChromaDB recommendations
"""

import requests
import json
import time

def test_complete_system():
    """Test the complete integration of fast multi-model system with ChromaDB recommendations"""
    base_url = "http://127.0.0.1:8001"
    
    print("Testing Complete Fast Multi-Model System with ChromaDB")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/healthz")
        if response.ok:
            health_data = response.json()
            print(f"API Status: {health_data['status']}")
            print(f"Fast Models: {health_data['fast_models']}")
            print(f"Original Model: {health_data['original_model']}")
            print(f"ChromaDB Available: {health_data.get('chromadb_available', False)}")
            print(f"Recommendations: {health_data['recs_index']}")
            print(f"Model Type: {health_data['model_type']}")
        else:
            print(f"Health check failed: {response.text}")
            return
    except Exception as e:
        print(f"Cannot connect to API: {e}")
        print("Make sure to start the API server with: uvicorn server.app:app --host 127.0.0.1 --port 8001")
        return
    
    # Test 2: Price Predictions with Different Product Types
    print(f"\n2. Testing Price Predictions...")
    test_cases = [
        {
            "name": "Jewelry Test",
            "data": {
                "product_name": "Men 18kt Gold Ring - 3.44gm",
                "brand": "tanishq",
                "gender": "men",
                "category": "ring",
                "fabric": None,
                "pattern": None,
                "color": "gold",
                "rating_count": 150,
                "discount_percent": 10.0
            }
        },
        {
            "name": "Watch Test", 
            "data": {
                "product_name": "Men Automatic Motion Watch",
                "brand": "titan",
                "gender": "men",
                "category": "watch",
                "fabric": None,
                "pattern": None,
                "color": "black",
                "rating_count": 200,
                "discount_percent": 15.0
            }
        },
        {
            "name": "Luxury Apparel Test",
            "data": {
                "product_name": "Designer Silk Saree with Embroidery",
                "brand": "sabyasachi",
                "gender": "women",
                "category": "saree",
                "fabric": "silk",
                "pattern": "embroidered",
                "color": "red",
                "rating_count": 50,
                "discount_percent": 5.0
            }
        },
        {
            "name": "Regular Apparel Test",
            "data": {
                "product_name": "Women Cotton Casual T-Shirt",
                "brand": "roadster",
                "gender": "women",
                "category": "tshirt",
                "fabric": "cotton",
                "pattern": "solid",
                "color": "blue",
                "rating_count": 500,
                "discount_percent": 30.0
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        
        try:
            response = requests.post(f"{base_url}/predict_price", json=test_case['data'])
            
            if response.ok:
                result = response.json()
                print(f"Predicted Price: Rs {result.get('predicted_price', 'N/A'):,.2f}")
                print(f"Product Type: {result.get('product_type', 'N/A')}")
                print(f"Model Type: {result.get('model_type', 'N/A')}")
                print(f"Product: {test_case['data']['product_name']}")
                
            else:
                print(f"Prediction failed: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 3: Recommendation System
    print(f"\n3. Testing Recommendation System...")
    try:
        response = requests.post(f"{base_url}/recommend_products", json={
            "query": "women cotton dress under 2000",
            "k": 5
        })
        
        if response.ok:
            results = response.json().get('results', [])
            print(f"Found {len(results)} recommendations")
            for i, result in enumerate(results[:3], 1):
                meta = result.get('metadata', {})
                print(f"   {i}. {meta.get('brand', 'Unknown')} - Rs {meta.get('discounted_price', 'N/A')}")
        else:
            print(f"Recommendations not available: {response.text}")
            
    except Exception as e:
        print(f"Recommendation test failed: {e}")
    
    print(f"\nComplete system testing finished!")
    print(f"\nYour Fast Multi-Model API with ChromaDB is ready to use!")
    print(f"   - API Server: http://127.0.0.1:8001")
    print(f"   - Start Streamlit: streamlit run streamlit_app.py")

if __name__ == "__main__":
    test_complete_system()
