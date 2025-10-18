import pandas as pd, chromadb
from sentence_transformers import SentenceTransformer

df = pd.read_parquet('myntra_cleaned.parquet').head(100_000)
texts = (df['brand'].fillna('') + ' ' + df['product_name'] + ' ' +
         df[['gender','category','fabric','pattern','color']].fillna('').agg(' '.join, axis=1))

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embs = model.encode(texts.tolist(), normalize_embeddings=True, batch_size=256, show_progress_bar=True)

client = chromadb.PersistentClient(path="./chroma_db")

# Recreate collection to ensure a clean index
try:
    client.delete_collection('fashion')
except Exception:
    pass
col = client.get_or_create_collection('fashion')
# Fill missing values for Chroma metadata
metadata_df = df[['brand','discounted_price','original_price','avg_rating','rating_count','gender','category','color']].fillna({
    'brand': 'unknown',
    'discounted_price': 0.0,
    'original_price': 0.0,
    'avg_rating': 0.0,
    'rating_count': 0,
    'gender': 'unisex',
    'category': 'other',
    'color': 'unknown'
})

ids = df.index.astype(str).tolist()
docs = texts.tolist()
metas = metadata_df.to_dict('records')
vecs = embs.tolist()

# Chroma has a max batch size; use safe chunking
batch_size = 5000
for start in range(0, len(ids), batch_size):
    end = start + batch_size
    col.add(
        ids=ids[start:end],
        documents=docs[start:end],
        metadatas=metas[start:end],
        embeddings=vecs[start:end]
    )

print('Indexed', len(ids), 'items')