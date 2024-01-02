import logging
import os

from pydantic import ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    postgres_user: str = Field("mainuser")
    postgres_password: SecretStr
    postgres_host: str = Field("localhost")
    pgport: int = Field(5433)
    postgres_db: str = Field("maindb")


class MainSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    uvicorn_host: str = Field("localhost")
    uvicorn_port: int = Field(8001)
    docs_username: str = Field("admin")
    docs_password: SecretStr
    auth_secret_key: SecretStr
    auth_algorithm: str = Field("HS256")
    auth_token_expire_days: int = Field(1)


class QueueSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    redis_host: str = Field("localhost")
    redis_password: SecretStr
    redis_port: int = Field(6379)
    redis_db: int = Field(0)


class ProjectSettings:
    def __init__(self, env_file: str, env_file_encoding: str):
        self.env_file = env_file
        self.env_file_encoding = env_file_encoding

        self.postgres = PostgresSettings(_env_file=self.env_file,
                                         _env_file_encoding=self.env_file_encoding)
        self.redis = QueueSettings(_env_file=self.env_file, _env_file_encoding=self.env_file_encoding)
        self.main = MainSettings(_env_file=self.env_file, _env_file_encoding=self.env_file_encoding)


def get_project_settings():
    root_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "environment")

    logging.info("Loading project settings")

    environment = os.environ.get("ENVIRONMENT", "dev")
    logging.info(f"Loading settings for environment: {environment}")

    match environment:
        case "dev":
            env_file = ".env.dev"
        case "prod":
            env_file = ".env.prod"
        case "test":
            env_file = ".env.test"
        case _:
            raise ValueError(f"Unknown environment: {environment}")

    env_file = os.path.join(root_dir, env_file)
    logging.info(f"Loading settings from file: {env_file}")

    return ProjectSettings(env_file=env_file, env_file_encoding="utf-8")


project_settings = get_project_settings()
