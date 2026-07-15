"""Configuration module for the AI Developer Assistant.

This module handles loading environment variables from a `.env` file,
validating settings, and providing a clean Config object to the application.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Find and load the .env file in the current project directory or parent directories
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


class ConfigError(Exception):
    """Custom exception class for configuration errors."""
    pass


class Config:
    """Class to manage configuration options loaded from environment variables."""

    def __init__(self) -> None:
        """Initialize configurations and perform standard validations."""
        self.api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.api_base: Optional[str] = os.getenv("GEMINI_API_BASE")
        self.model: Optional[str] = os.getenv("GEMINI_MODEL")
        
        temp_val = os.getenv("GEMINI_TEMPERATURE", "0.7").strip()
        try:
            self.temperature: float = float(temp_val)
        except ValueError:
            self.temperature = 0.7

        # Clean up values
        if self.api_key:
            self.api_key = self.api_key.strip()
        if self.api_base:
            self.api_base = self.api_base.strip()
        if self.model:
            self.model = self.model.strip()

    def validate(self) -> None:
        """Validate critical configuration settings.

        Raises:
            ConfigError: If required settings are missing or misconfigured.
        """
        # For Gemini, the API key is strictly required
        if not self.api_key:
            raise ConfigError(
                "GEMINI_API_KEY is not set in your .env file.\n"
                "Please copy .env.example to .env and configure your Gemini API Key."
            )

        # Enforce GEMINI_MODEL setting
        if not self.model:
            raise ConfigError(
                "GEMINI_MODEL is not set in your .env file.\n"
                "Please configure GEMINI_MODEL (e.g. gemini-3.5-flash) in your .env."
            )

        # Enforce GEMINI_TEMPERATURE ranges
        if self.temperature < 0.0 or self.temperature > 2.0:
            raise ConfigError(
                "GEMINI_TEMPERATURE must be a valid float between 0.0 and 2.0."
            )

    def get_summary(self) -> str:
        """Returns a string summary of current configuration (excluding sensitive keys)."""
        masked_key = "Not Set"
        if self.api_key:
            masked_key = f"{self.api_key[:6]}...{self.api_key[-4:]}" if len(self.api_key) > 10 else "Present"
            
        endpoint_display = self.api_base if self.api_base else "Default Gemini API"
        return (
            f"Endpoint: {endpoint_display}\n"
            f"Model:    {self.model}\n"
            f"API Key:  {masked_key}"
        )
