"""
Configuration management for the backend
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    API_TITLE: str = os.getenv("API_TITLE", "Mutual Fund NAV Tracker API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mutual_fund_tracker.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # Agent Configuration
    AGENT_CHECK_INTERVAL: int = int(os.getenv("AGENT_CHECK_INTERVAL", "300"))  # 5 minutes
    ALERT_COOLDOWN_HOURS: int = int(os.getenv("ALERT_COOLDOWN_HOURS", "1"))
    
    # Email Configuration
    EMAIL_ENABLED: bool = os.getenv("EMAIL_ENABLED", "False").lower() == "true"
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", "")
    RECEIVER_EMAIL: str = os.getenv("RECEIVER_EMAIL", "")
    
    # API Keys (for future use)
    MFAPI_BASE_URL: str = os.getenv("MFAPI_BASE_URL", "https://api.mfapi.in/mf")
    AMFI_BASE_URL: str = os.getenv("AMFI_BASE_URL", "https://portal.amfiindia.com")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    @classmethod
    def get_email_config(cls) -> dict:
        """Get email configuration dictionary"""
        return {
            'enabled': cls.EMAIL_ENABLED,
            'sender_email': cls.SENDER_EMAIL,
            'receiver_email': cls.RECEIVER_EMAIL,
            'smtp_server': cls.SMTP_SERVER,
            'smtp_port': cls.SMTP_PORT,
            'password': cls.SENDER_PASSWORD
        }

# Global config instance
config = Config()

