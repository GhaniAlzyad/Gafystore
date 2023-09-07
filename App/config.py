import os 

class config:
    DB_USER = os.getenv("DB_USER","postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD","password")
    DB_NAME = os.getenv("DB_NAME","gafystore")
    DB_HOST = os.getenv("DB_HOST","localhost")
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"