from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    APP_VERSION: str = "1.0"
    APP_NAME: str = "Todo App"

    DEBUG: bool = False


settings = Config()