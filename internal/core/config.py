from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    class Config:
        env_file = ".env"

settings = Settings()
