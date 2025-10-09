"""
Configuration settings for the OpenShift Partner Labs Agents application.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+mysqlconnector://username:password@localhost:3306/openshift_labs"
    )
    
    # Agno Configuration
    AGNO_API_KEY: str = os.getenv("AGNO_API_KEY", "")
    
    # Model Configuration
    MODEL_TYPE: str = os.getenv("MODEL_TYPE", "ollama")  # "ollama" or "openai"
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_TITLE: str = "OpenShift Partner Labs Agents API"
    API_VERSION: str = "1.0.0"
    
    # Session Configuration
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "your-secret-key-here")
    SESSION_EXPIRE_HOURS: int = int(os.getenv("SESSION_EXPIRE_HOURS", "24"))
    
    # Redis Configuration (for session storage)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # Agno UI default port
        "http://127.0.0.1:3000",
    ]
    
    # Agno UI Configuration
    AGNO_UI_URL: str = os.getenv("AGNO_UI_URL", "http://localhost:3000")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Development Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        required_vars = ["AGNO_API_KEY"]
        
        # Add model-specific requirements
        if cls.MODEL_TYPE == "openai":
            required_vars.append("OPENAI_API_KEY")
        elif cls.MODEL_TYPE == "ollama":
            # Ollama doesn't require API key for local usage
            pass
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

# Global config instance
config = Config()
