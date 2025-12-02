"""
Global variables and project settings
"""

import os
from pathlib import Path

# Directories
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
MODELS_DIR = DATA_DIR / "models"
DATABASE_PATH = DATA_DIR / "database.db"


# Create directories if they do not exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EMBEDDINGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Template settings
RECOMMENDER_CONFIG = {
    "n_arms": 10000,  # Maximum number of books
    "feature_dim": 10,  # Feature dimensionality
    "model_type": "linucb",
    "alpha": 0.5,  # LinUCB exploration parameter
    "batch_size": 5,  # Mini-batch actions size for update
    "item_config": EMBEDDINGS_DIR / "item_config.json",
    "model_path": MODELS_DIR / "linucb_model.json",
}

# Streamlit Settings
STREAMLIT_CONFIG = {
    "max_recommendations": 4,
    "page_title": "Recommender MVP",
    "layout": "wide",
    "api_url": "http://127.0.0.1:8000",
    "api_timeout": 5,
}

# FastAPI Settings
FASTAPI_CONFIG = {
    "title": "Recommender API",
    "version": "0.1.0",
    "host": "127.0.0.1",
    "port": 8000,
}
