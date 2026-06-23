from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ProFlow"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
