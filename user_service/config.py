import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///utilisateurs.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")




class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    TESTING = True