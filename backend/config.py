from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    
    DATABASE_URL: str 
    SECRET_KEY: str
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env" 

settings = Settings()
