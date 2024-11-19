"""
Ce module configure l'application Flask.

Classes:
- Config: Configuration principale pour l'application (base de données, JWT, etc.).
- TestConfig: Configuration spécifique pour les tests (utilise une base de données en mémoire).
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///utilisateurs.db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")
    PORT=os.getenv("PORT", "5000")