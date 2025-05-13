from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   DATABASE_URL: str
   HOST: str
   PORT: int
   DB_USER: str
   DB_PASSWORD: str
   DB_NAME: str

   class Config:
       env_file = ".env"

settings = Settings()
