"""
Security and Configuration Settings for Resume Screener API
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class SecurityConfig:
    """Security configuration settings"""
    
    # API Keys
    API_KEYS: List[str] = os.getenv("API_KEYS", "").split(",")
    REQUIRE_API_KEY: bool = os.getenv("REQUIRE_API_KEY", "true").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://localhost:3001"
    ).split(",")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "100"))
    
    # File Upload Limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc", ".txt"]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain"
    ]
    
    # Input Limits
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "50000"))  # 50KB of text
    MAX_BATCH_SIZE: int = int(os.getenv("MAX_BATCH_SIZE", "10"))
    
    # Request Limits
    MAX_REQUEST_SIZE_MB: int = int(os.getenv("MAX_REQUEST_SIZE_MB", "10"))
    
    @classmethod
    def is_valid_api_key(cls, api_key: str) -> bool:
        """Check if API key is valid"""
        if not cls.REQUIRE_API_KEY:
            return True
        return api_key in cls.API_KEYS and api_key != ""
    
    @classmethod
    def get_settings_info(cls) -> dict:
        """Get non-sensitive configuration info"""
        return {
            "rate_limit_enabled": cls.RATE_LIMIT_ENABLED,
            "rate_limit_per_minute": cls.RATE_LIMIT_PER_MINUTE,
            "max_file_size_mb": cls.MAX_FILE_SIZE_MB,
            "max_text_length": cls.MAX_TEXT_LENGTH,
            "max_batch_size": cls.MAX_BATCH_SIZE,
            "allowed_file_extensions": cls.ALLOWED_FILE_EXTENSIONS,
            "api_key_required": cls.REQUIRE_API_KEY
        }


# Create singleton instance
config = SecurityConfig()
