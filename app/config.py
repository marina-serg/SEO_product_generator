from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-3.1-flash-lite"
    gemini_timeout: int = 60
    max_retries: int = 3

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()