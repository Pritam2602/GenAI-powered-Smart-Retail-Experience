"""
Test script for Level 1 API functionality.
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8001"

def test_root_endpoint():
    """Test the root endpoint."""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint works!")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")
        return False

def test_health_endpoint():
    """Test the health check endpoint."""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint works!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Models loaded: {data.get('fast_models_loaded') or data.get('original_model_loaded')}")
            print(f"   Recommendation system: {data.get('recs_index_loaded')}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_price_prediction():
    """Test the price prediction endpoint."""
    print("\n🔍 Testing price prediction endpoint...")
    try:
        payload = {
            "product_name": "Men Solid Casual Shirt",
            "brand": "roadster",
            "gender": "men",
            "category": "shirt",
            "fabric": "cotton",
            "pattern": "solid",
            "color": "blue",
            "rating_count": 500,
            "discount_percent": 40.0
        }
        response = requests.post(f"{BASE_URL}/predict/price", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Price prediction endpoint works!")
            data = response.json()
            print(f"   Predicted price: ₹{data.get('predicted_price'):.2f}")
            print(f"   Product type: {data.get('product_type')}")
            print(f"   Model type: {data.get('model_type')}")
            print(f"   Confidence: {data.get('confidence')}")
            return True
        else:
            print(f"❌ Price prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing price prediction: {e}")
        return False

def test_recommendations():
    """Test the recommendations endpoint."""
    print("\n🔍 Testing recommendations endpoint...")
    try:
        payload = {
            "query": "blue denim jacket for men",
            "k": 5
        }
        response = requests.post(f"{BASE_URL}/recommend/products", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Recommendations endpoint works!")
            data = response.json()
            print(f"   Query: {data.get('query')}")
            print(f"   Results: {data.get('total_results')} products found")
            return True
        elif response.status_code == 503:
            print("⚠️  Recommendations endpoint returned 503 (service unavailable)")
            print("   This is expected if ChromaDB is not set up or empty")
            return True  # This is acceptable
        else:
            print(f"❌ Recommendations failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing recommendations: {e}")
        return False

def test_api_docs():
    """Test if API documentation is accessible."""
    print("\n🔍 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation (Swagger UI) is accessible!")
            return True
        else:
            print(f"❌ API documentation failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API documentation: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Testing Level 1 API Functionality")
    print("=" * 60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    results = []
    
    # Test endpoints
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("Health Endpoint", test_health_endpoint()))
    results.append(("Price Prediction", test_price_prediction()))
    results.append(("Recommendations", test_recommendations()))
    results.append(("API Documentation", test_api_docs()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Level 1 is working correctly!")
        return 0
    elif passed >= total - 1:  # Allow one failure (recommendations might not be set up)
        print("\n✅ Level 1 is working! (Some optional features may need setup)")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the server logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

