import logging
import os

from pydantic import ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresMainSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    postgres_main_user: str = Field("mainuser")
    postgres_main_password: SecretStr
    postgres_main_host: str = Field("localhost")
    postgres_main_port: int = Field(5433)
    postgres_main_db: str = Field("maindb")

    def get_db_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}"


class PostgresTestSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    postgres_test_user: str = Field("testuser")
    postgres_test_password: SecretStr
    postgres_test_host: str = Field("localhost")
    postgres_test_port: str = Field(5434)
    postgres_test_db: str = Field("testdb")


class MainSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    uvicorn_host: str = Field("localhost")
    uvicorn_port: int = Field(8001)
    docs_username: str = Field("admin")
    docs_password: SecretStr
    auth_secret_key: SecretStr
    auth_algorithm: str = Field("HS256")
    auth_token_expire_days: int = Field(1)


class ProjectSettings:
    def __init__(self, env_file: str, env_file_encoding: str):
        self.env_file = env_file
        self.env_file_encoding = env_file_encoding

        self.postgres_main_settings = PostgresMainSettings(_env_file=self.env_file,
                                                           _env_file_encoding=self.env_file_encoding)
        self.postgres_test_settings = PostgresTestSettings(_env_file=self.env_file,
                                                           _env_file_encoding=self.env_file_encoding)
        self.main_settings = MainSettings(_env_file=self.env_file, _env_file_encoding=self.env_file_encoding)


def get_project_settings():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging.info("Loading project settings")

    environment = os.environ.get("ENVIRONMENT", "dev")
    logging.info(f"Loading settings for environment: {environment}")

    env_file: str = ".env.prod" if environment == "prod" else ".env.dev"
    env_file = os.path.join(root_dir, env_file)
    logging.info(f"Loading settings from file: {env_file}")

    return ProjectSettings(env_file=env_file, env_file_encoding="utf-8")


project_settings = get_project_settings()
