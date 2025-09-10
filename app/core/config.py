import os 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


ENV = os.getenv("ENV", "development")  # default: development

if ENV in ("development", "testing"):
    dotenv_path = os.getenv("BACKEND_ENV_PATH", os.path.join(os.path.dirname(__file__), "../env/backend.env"))
    load_dotenv(dotenv_path)



class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config: 
        env_file = dotenv_path if ENV in ("development", "testing") else None
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    

settings = Settings()