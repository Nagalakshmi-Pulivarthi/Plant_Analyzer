"""
Configuration file for API keys and settings.
Store your API keys in environment variables or update this file directly.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys - Set these as environment variables for security
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

# API Settings
OPENAI_MODEL: str = "gpt-4o"  # Using gpt-4o for vision capabilities (optional, if still needed)
GEMINI_OBSERVATIONS_MODEL: str = "gemini-2.0-flash"   # For plant leaf image analysis
GEMINI_RECOMMENDATIONS_MODEL: str = "gemini-2.0-flash"  # For recommendations and severity
GEMINI_IMAGE_MODEL: str = "gemini-2.0-flash"            # Kept for reference (not used in V2)

# Application Settings
MAX_IMAGE_SIZE_MB: int = 10
ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/jpg", "image/png", "image/webp"]

def validate_config() -> bool:
    """Validate that all required API keys are set."""
    # GEMINI_API_KEY is required for all services now
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    # OPENAI_API_KEY is optional if using Gemini for observations
    return True

