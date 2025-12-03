GenAI-Powered Smart Retail Experience

A complete end-to-end AI system for intelligent price prediction, semantic product recommendations, trend analysis, and explainable AI — using FastAPI, Next.js, ChromaDB, and machine learning.

📌 Summary

This project has been upgraded through Levels 1–3 to become a professional, modular, and portfolio-ready retail AI application, including:

🧠 Multi-model price prediction

🔎 Semantic recommendations (Sentence Transformers + ChromaDB)

📊 Fashion trend analysis

🎨 Full Next.js frontend with animations

👁 Explainable AI

⚡ Modular backend (FastAPI)

🖥 Real-time API health monitoring

##  Project Structure

GenAI-powered Smart Retail Experience/
├── smart_retail/                   
│   ├── main.py                     # FastAPI app entry
│   ├── config.py                   # Configuration manager
│   ├── models/                     # Schemas and ML model loaders
│   ├── utils/                      # Utility modules
│   │   ├── preprocessing.py
│   │   ├── explainability.py
│   │   ├── fashion_trends.py
│   │   └── validators.py
│   ├── routes/                     # API endpoints
│   │   ├── health.py
│   │   ├── price_predict.py
│   │   ├── recommend.py
│   │   └── trends.py
│   ├── train/                      # 🔥 Training Scripts (NEW)
│   │   ├── train_price_prediction.py     # Train multi-model pricing system
│   │   └── create_embedding_model.py      # Create embedding index + ChromaDB
│   └── __init__.py
│
├── artifacts/                      # Auto-generated ML models (after training)
│   ├── fast_price_models.joblib
│   └── plots/                      # Metric plots for each model
│
├── chroma_db/                      # Auto-generated vector DB for recommender
│
├── frontend/                       # Next.js 14 application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.local
│
├── start_smart_retail.py           # Backend launcher
└── README.md                       # 📘 Documentation

```

##  Quick Start

### 1. Start Backend
```bash
python start_smart_retail.py
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

##  API Endpoints

### Health Check
- `GET /health/` - Comprehensive health status
- `GET /health/z` - Simple health check

### Price Prediction
- `POST /predict/price?explain=true` - Predict price with explanation

### Recommendations
- `POST /recommend/products` - Get product recommendations

### Trend Analysis
- `GET /trends/colors` - Trending colors
- `GET /trends/styles` - Trending styles
- `GET /trends/seasonal` - Seasonal trends
- `GET /trends/price` - Price trends
- `GET /trends/sustainability` - Sustainability trends
- `GET /trends/report` - Comprehensive trend report
- `POST /trends/brands` - Brand performance analysis

Features
🧠 Backend (FastAPI)

Multi-model price prediction (Apparel / Jewelry / Watches / Luxury)
Explainability (key factors, SHAP-like analysis)
Trend analysis API (colors, styles, price trends, sustainability)
Semantic recommendations (MiniLM embeddings + ChromaDB)
Robust route structure
Auto-generated API docs:

http://localhost:8001/docs
http://localhost:8001/redoc

🎨 Frontend (Next.js)

Real-time price prediction UI
Trend dashboards
Recommendation explorer
Live API status badge
Dark mode + TailwindCSS
Smooth animations and responsive design


Training Pipeline 

You now have a complete training workflow with two scripts:

1️⃣ train_price_prediction.py
📍 Location:

smart_retail/train/train_price_prediction.py

What it does:

Classifies products into types
Extracts enhanced features
Trains optimized XGBoost models for each product type
Evaluates (RMSE, MAE, R²)
Saves trained models to /artifacts
Generates metric plots for visualization

How to run:
cd smart_retail/train
python train_price_prediction.py

Outputs created:
artifacts/
│ fast_price_models.joblib
│
└── plots/
    ├── apparel/
    ├── jewelry/
    ├── watches/
    └── luxury_apparel/


Each product type folder contains:

metrics.png
actual_vs_pred.png
error_dist.png

2️⃣ create_embedding_model.py

📍 Location:

smart_retail/train/create_embedding_model.py

What it does:
Loads SentenceTransformer (all-MiniLM-L6-v2)
Generates product embeddings
Builds a ChromaDB vector index
Saves the index into /chroma_db/

How to run:
cd smart_retail/train
python create_embedding_model.py

Outputs created:
chroma_db/
│ collections/
│ index_state.json
│ embeddings.bin

These embeddings power the semantic recommender used in your API.

