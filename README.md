# 🛍️ GenAI-powered Smart Retail Experience

A professional, production-ready AI-powered fashion recommendation and price prediction system built with FastAPI. This project demonstrates advanced machine learning techniques, vector databases, and modern API design.

## ✨ Features

### 🤖 AI-Powered Price Prediction
- **Multi-Model System**: Specialized ML models for different product types
  - **Jewelry Model**: Optimized for gold, silver, diamonds, and precious stones
  - **Watch Model**: Specialized for timepieces, movements, and luxury brands
  - **Luxury Apparel Model**: For designer, premium, and high-end fashion
  - **Standard Apparel Model**: For regular clothing and accessories
- **Automatic Product Classification**: Intelligent product type detection
- **Realistic Price Constraints**: Domain-specific price ranges
- **High Accuracy**: Trained on large fashion datasets

### 🔍 Smart Product Recommendations
- **Semantic Search**: Vector-based product recommendations using sentence transformers
- **Vector Database**: ChromaDB for efficient similarity search
- **Cosine Similarity**: Advanced matching algorithms
- **Configurable Results**: Flexible number of recommendations (1-50)

### 📊 Professional API
- **FastAPI Framework**: High-performance, modern API framework
- **Auto-Generated Documentation**: Interactive Swagger UI and ReDoc
- **Comprehensive Validation**: Input validation and error handling
- **Health Monitoring**: Health check endpoints for system monitoring
- **Logging**: Professional logging and error tracking

### 🏗️ Modular Architecture
- **Clean Code Structure**: Professional, maintainable codebase
- **Separation of Concerns**: Routes, models, and utilities organized separately
- **Type Safety**: Pydantic models for request/response validation
- **Configuration Management**: Centralized settings management

## 📁 Project Structure

```
GenAI-powered Smart Retail Experience/
├── smart_retail/                 # Backend application directory
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── app.py                    # Alternative entry point
│   ├── config.py                 # Configuration management
│   ├── models/                   # ML models and data models
│   │   ├── __init__.py
│   │   ├── data_models.py        # Pydantic models
│   │   └── ml_models.py          # ML model management
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py             # Health check endpoints
│   │   ├── price_predict.py      # Price prediction endpoints
│   │   ├── recommend.py          # Recommendation endpoints
│   │   └── trends.py             # Trend analysis endpoints
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── preprocessing.py      # Data preprocessing
│   │   ├── fashion_trends.py     # Trend analysis
│   │   ├── explainability.py     # Explainability utilities
│   │   └── validators.py         # Input validation
│   ├── static/                   # Static files
│   ├── tests/                    # Test files
│   └── README.md                 # Module documentation
├── frontend/                     # Frontend application (Next.js)
│   ├── app/                      # Next.js app directory
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Home page
│   │   └── globals.css           # Global styles
│   ├── components/               # React components
│   │   ├── Header.tsx            # Header component
│   │   ├── PricePrediction.tsx   # Price prediction component
│   │   ├── Recommendations.tsx   # Recommendations component
│   │   └── TrendAnalysis.tsx     # Trend analysis component
│   ├── lib/                      # Utilities
│   │   └── api.ts                # API service
│   ├── package.json              # Frontend dependencies
│   ├── tailwind.config.js        # TailwindCSS configuration
│   ├── tsconfig.json             # TypeScript configuration
│   └── next.config.js            # Next.js configuration
├── artifacts/                    # Trained ML models
│   ├── fast_price_models_api.joblib
│   ├── price_model_improved.joblib
│   └── fallback_model.joblib
├── chroma_db/                    # Vector database
├── Data_Collection.ipynb         # Data collection notebook
├── EDA.ipynb                     # Exploratory data analysis
├── start_smart_retail.py         # Backend startup script
├── requirements.txt              # Backend dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── Procfile                      # Process configuration
├── render.yaml                   # Render deployment configuration
└── README.md                     # This file
```

## 🚀 Quick Start

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "GenAI-powered Smart Retail Experience"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   cd smart_retail
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   export HOST="0.0.0.0"
   export PORT="8001"
   ```

5. **Start the backend server**:
   ```bash
   python start_smart_retail.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local and set NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
   ```

4. **Start the frontend server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open in browser**:
   ```
   http://localhost:3000
   ```

### Running the Application

#### Backend (API Server)

**Option 1: Using the startup script (Recommended)**
```bash
python start_smart_retail.py
```

**Option 2: Using the module directly**
```bash
python -m smart_retail.main
```

**Option 3: Using uvicorn**
```bash
uvicorn smart_retail.main:app --host 0.0.0.0 --port 8001 --reload
```

**Option 4: Using Docker**
```bash
docker-compose up --build
```

#### Frontend (Web Application)

**Development Mode**
```bash
cd frontend
npm run dev
# or
yarn dev
```

**Production Build**
```bash
cd frontend
npm run build
npm start
# or
yarn build
yarn start
```

The frontend will be available at http://localhost:3000

## 📚 API Documentation

Once the server is running, visit:

- **Interactive API Docs (Swagger UI)**: http://localhost:8001/docs
- **ReDoc Documentation**: http://localhost:8001/redoc
- **API Root**: http://localhost:8001/

## 🔗 API Endpoints

### Health Check
- `GET /health/` - Comprehensive health status
- `GET /health/z` - Simple health check

### Price Prediction
- `POST /predict/price` - Predict product price
  - **Request Body**: Product details (name, brand, gender, category, etc.)
  - **Response**: Predicted price, product type, model type, confidence

### Recommendations
- `POST /recommend/products` - Get product recommendations
  - **Request Body**: Search query and number of results
  - **Response**: List of recommended products with similarity scores

### Trend Analysis
- `GET /trends/colors?timeframe=30d` - Get trending colors
- `GET /trends/styles?category=all` - Get trending styles
- `GET /trends/seasonal?season=winter` - Get seasonal trends
- `GET /trends/price?category=all` - Get price trends
- `GET /trends/sustainability` - Get sustainability trends
- `GET /trends/report` - Get comprehensive trend report
- `POST /trends/brands` - Analyze brand performance

## 📖 Example Usage

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
# Output: {
#     "predicted_price": 899.50,
#     "product_type": "apparel",
#     "model_type": "fast_multi_model",
#     "confidence": "Medium",
#     "timestamp": "2024-01-15T10:30:00"
# }
```

### Product Recommendations

```python
# Get product recommendations
response = requests.post("http://localhost:8001/recommend/products", json={
    "query": "blue denim jacket for men",
    "k": 10
})

print(response.json())
# Output: {
#     "results": [...],
#     "query": "blue denim jacket for men",
#     "total_results": 10,
#     "timestamp": "2024-01-15T10:30:00"
# }
```

## 🧠 Model Architecture

### Price Prediction Models
- **Fast Multi-Model System**: Specialized models for different product types
- **Feature Engineering**: Advanced feature extraction (brand prestige, materials, styles)
- **Price Constraints**: Realistic price ranges based on product type
- **Fallback System**: Multiple model fallbacks for reliability

### Recommendation System
- **Vector Database**: ChromaDB for efficient similarity search
- **Embedding Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Similarity Search**: Cosine similarity for finding similar products
- **Scalable**: Handles large product catalogs efficiently

## 🔧 Configuration

The application uses a centralized configuration system in `smart_retail/config.py`:

- **Model Paths**: Automatic model discovery and loading
- **Database Settings**: ChromaDB configuration
- **API Settings**: CORS, documentation, and server settings
- **Price Constraints**: Realistic price ranges for different product types
- **Brand Prestige Scores**: Brand-specific price adjustments

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=smart_retail

# Run specific test file
pytest tests/test_price_predict.py
```

## 🚀 Deployment

### Backend Deployment

**Using Docker**
```bash
# Build image
docker build -t smart-retail-api .

# Run container
docker run -p 8001:8001 smart-retail-api
```

**Using Docker Compose**
```bash
docker-compose up --build
```

**Using Render/Railway**
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn smart_retail.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables (if needed)

### Frontend Deployment

**Using Vercel (Recommended)**
1. Push your code to GitHub
2. Import your repository to Vercel
3. Set environment variables (NEXT_PUBLIC_API_BASE_URL)
4. Deploy!

**Using Netlify**
1. Build the application: `npm run build`
2. Deploy the `out` directory to Netlify
3. Set environment variables in Netlify dashboard

**Using Docker**
```bash
cd frontend
docker build -t smart-retail-frontend .
docker run -p 3000:3000 smart-retail-frontend
```

## 📊 Data Collection

The project includes notebooks for data collection:

- **Data_Collection.ipynb**: Scrapes Flipkart and Myntra for product data
- **EDA.ipynb**: Exploratory data analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **Sentence Transformers** for embedding models
- **ChromaDB** for vector database functionality
- **Scikit-learn** for machine learning capabilities
- **Pydantic** for data validation

## 🔮 Future Enhancements

- [x] Frontend UI (React/Next.js) ✅ **Level 3 Complete**
- [x] Advanced trend analysis ✅ **Level 2 Complete**
- [x] Explainable AI (Feature importance) ✅ **Level 2 Complete**
- [ ] User authentication and personalization
- [ ] Real-time analytics dashboard
- [ ] Image-based recommendations
- [ ] Multi-language support
- [ ] SHAP/LIME explainability (optional)
- [ ] A/B testing framework

## 📞 Contact

For questions or suggestions, please open an issue or contact the maintainers.

---

**Built with ❤️ for the GenAI-powered Smart Retail Experience**
