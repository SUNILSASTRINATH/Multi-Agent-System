from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    OLLAMA_MODEL: str = Field(default="mistral", description="Ollama model (e.g., mistral, llama3)")
    OLLAMA_HOST: str | None = Field(default=None, description="Override Ollama host, e.g., http://localhost:11434")

settings = Settings()
