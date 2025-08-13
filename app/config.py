import os
from datetime import timedelta


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///task_manager.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    SWAGGER = {
        "title": "Task Manager API",
        "uiversion": 3,
        "openapi": "3.0.3",
    }


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret"


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


def get_config(name: str | None):
    mapping = {
        "testing": TestConfig,
        "development": DevConfig,
        "production": ProdConfig,
        None: DevConfig,
    }
    return mapping.get(name, DevConfig)