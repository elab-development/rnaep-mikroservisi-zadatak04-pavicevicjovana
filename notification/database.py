from pydantic_settings import BaseSettings, SettingsConfigDict
from redis_om import get_redis_connection


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password or None,
    decode_responses=True
)
