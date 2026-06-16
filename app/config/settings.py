
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    UPLOAD_DIR:str
    REPORT_DIR:str
    VECTOR_DB_DIR:str

    class Config:
        env_file=".env"

settings=Settings()
