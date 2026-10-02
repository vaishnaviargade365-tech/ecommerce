"""
Configuration module for the Flask e-commerce backend.
Loads configuration from environment variables defined in .env.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Locate the .env file in the backend directory or project root
backend_dir = Path(__file__).resolve().parent
env_path = backend_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to general load_dotenv
    load_dotenv()


class Config:
    """Application configuration settings."""

    # MongoDB Atlas Connection URI
    # Fallback to local MongoDB if not specified in .env
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/ecommerce_db"
    )

    # Database Name in MongoDB
    DB_NAME = os.getenv("DB_NAME", "ecommerce_db")

    # Flask Server Port
    PORT = int(os.getenv("PORT", 5000))

    # Flask Environment & Debug Mode
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    # Secret key for security operations and token hashing
    SECRET_KEY = os.getenv("SECRET_KEY", "student-ecommerce-default-secret-key-2026")

    # JSON response settings
    JSON_SORT_KEYS = False
