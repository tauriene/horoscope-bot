from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    bot_token: str
    logging_level: str
    redis_host: str
    redis_port: int
    redis_password: str

    model_config = SettingsConfigDict(
        env_file=root_dir / ".env", env_file_encoding="utf-8"
    )


config = Settings()
