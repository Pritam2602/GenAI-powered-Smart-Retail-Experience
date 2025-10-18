#!/usr/bin/env python3
"""Test if images are working in recommendations"""

import requests

def test_recommendations():
    response = requests.post('http://127.0.0.1:8001/recommend_products', 
                           json={'query': 'blue denim jacket for men', 'k': 3})
    
    if response.ok:
        results = response.json().get('results', [])
        print(f'Found {len(results)} recommendations')
        
        for i, result in enumerate(results[:2], 1):
            meta = result.get('metadata', {})
            brand = meta.get('brand', 'Unknown')
            img_url = meta.get('img', 'No image')
            print(f'Item {i}: {brand}')
            print(f'  Image URL: {img_url[:100]}...')
            print()
    else:
        print('Error:', response.text)

if __name__ == "__main__":
    test_recommendations()
