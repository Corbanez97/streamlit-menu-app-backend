from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    
    DATABASE_URL: str 

    class Config:
        env_file = ".env" 

settings = Settings()
