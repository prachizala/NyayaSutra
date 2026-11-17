"""
NyayaSutra Core Configuration & Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NyayaSutra (न्यायसूत्र)"
    app_version: str = "0.1.0"
    env: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-key-replace-in-production"

    # Multimodal & External AI Keys
    gemini_api_key: str = ""
    bhashini_api_key: str = ""
    sarvam_api_key: str = ""

    # Supported Indian Languages
    supported_languages: list[str] = [
        "gu",  # Gujarati
        "hi",  # Hindi
        "mr",  # Marathi
        "ta",  # Tamil
        "te",  # Telugu
        "bn",  # Bengali
        "en",  # English
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
