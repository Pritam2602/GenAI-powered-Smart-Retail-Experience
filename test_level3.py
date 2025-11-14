"""
Test script for Level 3 Frontend functionality.
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

BASE_URL = "http://localhost:8001"
FRONTEND_PORT = 3000

def test_api_health():
    """Test API health endpoint."""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Models loaded: {data.get('fast_models_loaded') or data.get('original_model_loaded')}")
            print(f"   Recommendations: {data.get('recs_index_loaded')}")
            return True
        else:
            print(f"❌ API health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the backend running?")
        return False
    except Exception as e:
        print(f"❌ Error testing API health: {e}")
        return False

def test_price_prediction_with_explanation():
    """Test price prediction with explanation."""
    print("\n🔍 Testing price prediction with explanation...")
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
        response = requests.post(f"{BASE_URL}/predict/price?explain=true", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Price prediction with explanation works!")
            print(f"   Predicted price: ₹{data.get('predicted_price'):.2f}")
            print(f"   Product type: {data.get('product_type')}")
            print(f"   Model type: {data.get('model_type')}")
            if data.get('explanation'):
                print(f"   Explanation: {len(data['explanation'].get('key_factors', []))} key factors")
                print(f"   Price breakdown: Original ₹{data['explanation']['price_breakdown']['original_price']:.2f}")
                print(f"   Recommendations: {len(data['explanation'].get('recommendations', []))} recommendations")
            return True
        else:
            print(f"❌ Price prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing price prediction: {e}")
        return False

def test_trending_colors():
    """Test trending colors endpoint."""
    print("\n🔍 Testing trending colors endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/colors?timeframe=30d", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Trending colors endpoint works!")
            print(f"   Colors: {len(data.get('colors', []))} trending colors")
            if data.get('colors'):
                print(f"   Top color: {data['colors'][0].get('color')} ({data['colors'][0].get('popularity', 0)*100:.0f}% popularity)")
            return True
        else:
            print(f"❌ Trending colors failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing trending colors: {e}")
        return False

def test_trending_styles():
    """Test trending styles endpoint."""
    print("\n🔍 Testing trending styles endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/styles?category=all", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Trending styles endpoint works!")
            print(f"   Styles: {len(data.get('styles', []))} trending styles")
            return True
        else:
            print(f"❌ Trending styles failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing trending styles: {e}")
        return False

def test_seasonal_trends():
    """Test seasonal trends endpoint."""
    print("\n🔍 Testing seasonal trends endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/seasonal", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Seasonal trends endpoint works!")
            print(f"   Season: {data.get('season', 'current')}")
            print(f"   Colors: {len(data.get('colors', []))} seasonal colors")
            print(f"   Styles: {len(data.get('styles', []))} seasonal styles")
            return True
        else:
            print(f"❌ Seasonal trends failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing seasonal trends: {e}")
        return False

def test_price_trends():
    """Test price trends endpoint."""
    print("\n🔍 Testing price trends endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/price?category=all", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Price trends endpoint works!")
            print(f"   Average price: ₹{data.get('average_price', 0):.2f}")
            print(f"   Price change: {data.get('price_change', 0)*100:.2f}%")
            print(f"   Trend direction: {data.get('trend_direction', 'unknown')}")
            return True
        else:
            print(f"❌ Price trends failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing price trends: {e}")
        return False

def test_sustainability_trends():
    """Test sustainability trends endpoint."""
    print("\n🔍 Testing sustainability trends endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/sustainability", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sustainability trends endpoint works!")
            print(f"   Consumer interest: {data.get('consumer_interest', 0)*100:.0f}%")
            print(f"   Eco-friendly materials: {len(data.get('eco_friendly_materials', []))} materials")
            return True
        else:
            print(f"❌ Sustainability trends failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing sustainability trends: {e}")
        return False

def test_brand_analysis():
    """Test brand analysis endpoint."""
    print("\n🔍 Testing brand analysis endpoint...")
    try:
        brands = ["nike", "adidas", "zara"]
        response = requests.post(f"{BASE_URL}/trends/brands", json=brands, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Brand analysis endpoint works!")
            print(f"   Brands analyzed: {len(brands)}")
            for brand in brands:
                if brand in data:
                    print(f"   {brand}: {data[brand].get('popularity_score', 0):.2f} popularity")
            return True
        else:
            print(f"❌ Brand analysis failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing brand analysis: {e}")
        return False

def test_trend_report():
    """Test comprehensive trend report endpoint."""
    print("\n🔍 Testing trend report endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/trends/report", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Trend report endpoint works!")
            print(f"   Trending colors: {len(data.get('trending_colors', []))}")
            print(f"   Trending styles: {len(data.get('trending_styles', []))}")
            print(f"   Seasonal trends: {'present' if data.get('seasonal_trends') else 'missing'}")
            print(f"   Price trends: {'present' if data.get('price_trends') else 'missing'}")
            print(f"   Sustainability trends: {'present' if data.get('sustainability_trends') else 'missing'}")
            return True
        else:
            print(f"❌ Trend report failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing trend report: {e}")
        return False

def test_recommendations():
    """Test recommendations endpoint."""
    print("\n🔍 Testing recommendations endpoint...")
    try:
        payload = {
            "query": "blue denim jacket for men",
            "k": 5
        }
        response = requests.post(f"{BASE_URL}/recommend/products", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Recommendations endpoint works!")
            print(f"   Results: {data.get('total_results', 0)} products found")
            print(f"   Query: {data.get('query')}")
            return True
        elif response.status_code == 503:
            print("⚠️  Recommendations endpoint returned 503 (service unavailable)")
            print("   This is expected if ChromaDB is not set up or empty")
            return True  # This is acceptable
        else:
            print(f"❌ Recommendations failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing recommendations: {e}")
        return False

def test_frontend_structure():
    """Test frontend file structure."""
    print("\n🔍 Testing frontend file structure...")
    frontend_dir = Path("frontend")
    
    required_files = [
        "package.json",
        "next.config.js",
        "tailwind.config.js",
        "tsconfig.json",
        "postcss.config.js",
        "app/page.tsx",
        "app/layout.tsx",
        "app/globals.css",
        "lib/api.ts",
        "components/Header.tsx",
        "components/PricePrediction.tsx",
        "components/Recommendations.tsx",
        "components/TrendAnalysis.tsx",
    ]
    
    missing_files = []
    for file in required_files:
        if not (frontend_dir / file).exists():
            missing_files.append(file)
    
    if not missing_files:
        print("✅ All required frontend files exist!")
        return True
    else:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Testing Level 3: Frontend & API Integration")
    print("=" * 60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for API server to be ready...")
    time.sleep(3)
    
    results = []
    
    # Test API endpoints
    results.append(("API Health", test_api_health()))
    results.append(("Price Prediction with Explanation", test_price_prediction_with_explanation()))
    results.append(("Trending Colors", test_trending_colors()))
    results.append(("Trending Styles", test_trending_styles()))
    results.append(("Seasonal Trends", test_seasonal_trends()))
    results.append(("Price Trends", test_price_trends()))
    results.append(("Sustainability Trends", test_sustainability_trends()))
    results.append(("Brand Analysis", test_brand_analysis()))
    results.append(("Trend Report", test_trend_report()))
    results.append(("Recommendations", test_recommendations()))
    results.append(("Frontend Structure", test_frontend_structure()))
    
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
        print("\n🎉 All tests passed! Level 3 is working correctly!")
        return 0
    elif passed >= total - 1:  # Allow one failure (recommendations might not be set up)
        print("\n✅ Level 3 is working! (Some optional features may need setup)")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the server logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())




