#!/usr/bin/env python3
"""
Fix image URLs and rebuild ChromaDB with proper image metadata
"""

import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import re

def extract_first_image_url(img_string):
    """Extract the first (best quality) image URL from semicolon-separated string"""
    if pd.isna(img_string) or not img_string:
        return None
    
    # Split by semicolon and take the first URL
    urls = str(img_string).split(';')
    if urls:
        # Clean up the URL (remove any extra whitespace/newlines)
        first_url = urls[0].strip()
        # Remove any trailing newlines or spaces
        first_url = first_url.replace('\n', '').strip()
        return first_url if first_url else None
    return None

def rebuild_chroma_with_images():
    """Rebuild ChromaDB with proper image URLs"""
    print("Loading data...")
    df = pd.read_parquet('myntra_cleaned.parquet').head(100_000)
    
    print("Processing image URLs...")
    # Extract first image URL from each product
    df['first_img_url'] = df['img'].apply(extract_first_image_url)
    
    # Create text for embedding
    texts = (df['brand'].fillna('') + ' ' + df['product_name'] + ' ' +
             df[['gender','category','fabric','pattern','color']].fillna('').agg(' '.join, axis=1))
    
    print("Loading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embs = model.encode(texts.tolist(), normalize_embeddings=True, batch_size=256, show_progress_bar=True)
    
    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection
    try:
        client.delete_collection('fashion')
        print("Deleted existing collection")
    except Exception:
        pass
    
    # Create new collection
    col = client.get_or_create_collection('fashion')
    
    # Prepare metadata with proper image URLs
    metadata_df = df[['brand','discounted_price','original_price','avg_rating','rating_count','gender','category','color','first_img_url']].copy()
    metadata_df = metadata_df.fillna({
        'brand': 'unknown',
        'discounted_price': 0.0,
        'original_price': 0.0,
        'avg_rating': 0.0,
        'rating_count': 0,
        'gender': 'unisex',
        'category': 'other',
        'color': 'unknown'
    })
    # Handle image URLs separately
    metadata_df['first_img_url'] = metadata_df['first_img_url'].fillna('')
    
    # Rename the image column to 'img' for consistency
    metadata_df = metadata_df.rename(columns={'first_img_url': 'img'})
    
    ids = df.index.astype(str).tolist()
    docs = texts.tolist()
    metas = metadata_df.to_dict('records')
    vecs = embs.tolist()
    
    print("Adding items to ChromaDB...")
    # Chroma has a max batch size; use safe chunking
    batch_size = 5000
    for start in range(0, len(ids), batch_size):
        end = start + batch_size
        print(f"Processing batch {start//batch_size + 1}/{(len(ids)-1)//batch_size + 1}")
        col.add(
            ids=ids[start:end],
            documents=docs[start:end],
            metadatas=metas[start:end],
            embeddings=vecs[start:end]
        )
    
    print(f'Successfully indexed {len(ids)} items with proper image URLs!')
    
    # Test a few items
    print("\nTesting image URLs:")
    result = col.get(limit=3, include=['metadatas'])
    for i, meta in enumerate(result['metadatas'][:3]):
        print(f"Item {i+1}: {meta.get('brand', 'Unknown')} - {meta.get('img', 'No image')[:100]}...")

if __name__ == "__main__":
    rebuild_chroma_with_images()
