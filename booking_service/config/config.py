from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Raga Roads Booking Service"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Artist allocation booking platform"

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "raga_roads"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "admin123"

    ARTIST_SERVICE_URL: str = "http://artist_service:8001"
    CONCERT_SERVICE_URL: str = "http://concert_service:8002"

    SECRET_KEY: str = "raga-roads-secret-key"
    ALGORITHM: str = "HS256"

settings = Settings()
