#!/usr/bin/env python3
"""
Test script to verify the local API and Streamlit connection.
"""

import requests
import time

def test_api_connection():
    """Test the local API server."""
    print("Testing local API server...")
    try:
        response = requests.get("http://127.0.0.1:8001/healthz", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("API Server: Working")
            print(f"   Status: {data.get('status')}")
            print(f"   Fast Models: {data.get('fast_models_loaded')}")
            print(f"   Recommendations: {data.get('recs_index_loaded')}")
            print(f"   Model Type: {data.get('model_type_in_use')}")
            return True
        else:
            print(f"API Server: Error {response.status_code}")
            return False
    except Exception as e:
        print(f"API Server: Connection failed - {e}")
        return False

def test_streamlit_connection():
    """Test the Streamlit app."""
    print("\nTesting Streamlit app...")
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("Streamlit App: Working")
            return True
        else:
            print(f"Streamlit App: Error {response.status_code}")
            return False
    except Exception as e:
        print(f"Streamlit App: Connection failed - {e}")
        return False

def test_prediction():
    """Test a sample prediction."""
    print("\nTesting price prediction...")
    try:
        payload = {
            "product_name": "Men Solid Casual Shirt",
            "brand": "roadster",
            "gender": "men",
            "category": "shirt",
            "fabric": "cotton",
            "pattern": "solid",
            "color": "blue",
            "number_of_ratings": 500,
            "discount_percentage": 40
        }
        
        response = requests.post("http://127.0.0.1:8001/predict_price", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("Price Prediction: Working")
            print(f"   Predicted Price: Rs {data.get('predicted_price', 'N/A'):,.2f}")
            print(f"   Product Type: {data.get('product_type', 'N/A')}")
            return True
        else:
            print(f"Price Prediction: Error {response.status_code}")
            return False
    except Exception as e:
        print(f"Price Prediction: Failed - {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Local GenAI Fashion Hub System")
    print("=" * 50)
    
    api_ok = test_api_connection()
    streamlit_ok = test_streamlit_connection()
    prediction_ok = test_prediction()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"   API Server: {'Working' if api_ok else 'Failed'}")
    print(f"   Streamlit App: {'Working' if streamlit_ok else 'Failed'}")
    print(f"   Price Prediction: {'Working' if prediction_ok else 'Failed'}")
    
    if api_ok and streamlit_ok and prediction_ok:
        print("\nAll systems are working! Your local setup is ready.")
        print("\nAccess your applications:")
        print("   - Streamlit App: http://localhost:8501")
        print("   - API Server: http://127.0.0.1:8001")
        print("   - API Health: http://127.0.0.1:8001/healthz")
    else:
        print("\nSome systems are not working. Please check the errors above.")

if __name__ == "__main__":
    main()
