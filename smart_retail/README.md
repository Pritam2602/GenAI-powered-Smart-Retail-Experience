# GenAI-powered Smart Retail Experience

A modular, professional AI-powered fashion recommendation and price prediction system built with FastAPI.

## 🚀 Features

- **AI Price Prediction**: Multi-model system with specialized models for different product types
- **Smart Recommendations**: Vector-based product recommendations using sentence transformers
- **Modular Architecture**: Clean, maintainable code structure
- **Professional API**: Auto-generated documentation with FastAPI
- **Trend Analysis**: Fashion trend insights and analytics
- **Input Validation**: Comprehensive data validation and sanitization

## 📁 Project Structure

```
smart_retail/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── models/                # ML models and data models
│   ├── __init__.py
│   ├── data_models.py     # Pydantic models
│   └── ml_models.py       # ML model management
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── health.py          # Health check endpoints
│   ├── price_predict.py  # Price prediction endpoints
│   └── recommend.py       # Recommendation endpoints
└── utils/                 # Utility functions
    ├── __init__.py
    ├── preprocessing.py   # Data preprocessing
    ├── fashion_trends.py  # Trend analysis
    └── validators.py      # Input validation
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd smart_retail
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   export API_BASE_URL="http://localhost:8001"
   export HOST="0.0.0.0"
   export PORT="8001"
   ```

## 🚀 Running the Application

### Development Mode
```bash
python -m smart_retail.main
```

### Production Mode
```bash
uvicorn smart_retail.main:app --host 0.0.0.0 --port 8001
```

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8001/docs
- **ReDoc Documentation**: http://localhost:8001/redoc

## 🔗 API Endpoints

### Health Check
- `GET /health/` - Comprehensive health status
- `GET /health/z` - Simple health check

### Price Prediction
- `POST /predict/price` - Predict product price

### Recommendations
- `POST /recommend/products` - Get product recommendations

## 🧠 Model Architecture

### Price Prediction Models
- **Fast Multi-Model System**: Specialized models for different product types
  - Jewelry Model: Gold, silver, diamonds, precious stones
  - Watch Model: Timepieces, movements, luxury brands
  - Luxury Apparel Model: Designer, premium, high-end fashion
  - Standard Apparel Model: Regular clothing and accessories

### Recommendation System
- **Vector Database**: ChromaDB for efficient similarity search
- **Embedding Model**: Sentence Transformers for text embeddings
- **Similarity Search**: Cosine similarity for recommendations

## 🔧 Configuration

The application uses a centralized configuration system in `config.py`:

- **Model Paths**: Automatic model discovery and loading
- **Database Settings**: ChromaDB configuration
- **API Settings**: CORS, documentation, and server settings
- **Price Constraints**: Realistic price ranges for different product types

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=smart_retail
```

## 📊 Example Usage

### Price Prediction
```python
import requests

# Predict price for a product
response = requests.post("http://localhost:8001/predict/price", json={
    "product_name": "Men Solid Casual Shirt",
    "brand": "roadster",
    "gender": "men",
    "category": "shirt",
    "fabric": "cotton",
    "pattern": "solid",
    "color": "blue",
    "rating_count": 500,
    "discount_percent": 40.0
})

print(response.json())
```

### Product Recommendations
```python
# Get product recommendations
response = requests.post("http://localhost:8001/recommend/products", json={
    "query": "blue denim jacket for men",
    "k": 10
})

print(response.json())
```

## 🚀 Deployment

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["uvicorn", "smart_retail.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Using Render/Railway
1. Connect your repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn smart_retail.main:app --host 0.0.0.0 --port $PORT`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Sentence Transformers for embedding models
- ChromaDB for vector database functionality
- Scikit-learn for machine learning capabilities
