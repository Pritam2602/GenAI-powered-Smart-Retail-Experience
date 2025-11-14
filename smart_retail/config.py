"""
Configuration management for the Smart Retail API.
Handles environment variables and application settings.
"""

import os
from typing import Dict, Any
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    API_TITLE: str = "GenAI Fashion Hub API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered fashion recommendation and price prediction system"
    
    # Model Paths
    ARTIFACTS_DIR: Path = BASE_DIR / "artifacts"
    CHROMA_DB_DIR: Path = BASE_DIR / "chroma_db"
    
    # Model Files
    FAST_MODELS_PATH: Path = ARTIFACTS_DIR / "fast_price_models_api.joblib"
    ORIGINAL_MODEL_PATH: Path = ARTIFACTS_DIR / "price_model_improved.joblib"
    FALLBACK_MODEL_PATH: Path = ARTIFACTS_DIR / "fallback_model.joblib"
    
    # Database Configuration
    CHROMA_COLLECTION_NAME: str = "fashion"
    
    # Model Configuration
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Price Constraints
    PRICE_CONSTRAINTS: Dict[str, tuple] = {
        'jewelry': (100, 200000),
        'watches': (500, 100000),
        'luxury_apparel': (1000, 50000),
        'apparel': (50, 10000)
    }
    
    # Brand Prestige Scores (can be loaded from external source)
    BRAND_PRESTIGE_SCORES: Dict[str, float] = {
        'nike': 2500.0,
        'adidas': 2200.0,
        'zara': 1500.0,
        'h&m': 800.0,
        'roadster': 600.0,
        'levis': 1800.0,
        'puma': 1200.0,
        'rebook': 1000.0
    }
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    @classmethod
    def get_env_variable(cls, key: str, default: Any = None) -> Any:
        """Get environment variable with fallback to default."""
        return os.getenv(key, default)
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.ARTIFACTS_DIR.mkdir(exist_ok=True)
        cls.CHROMA_DB_DIR.mkdir(exist_ok=True)

# Global settings instance
settings = Settings()
