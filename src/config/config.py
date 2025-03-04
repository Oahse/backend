import os

class Settings:
    PROJECT_NAME: str = "FastAPI App"
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
