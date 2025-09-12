from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
  DATABASE_URL: str
  ALEMBIC_URL: str

  class Config:
    env_file = ".env"
    extra = "ignore"

app_settings = AppSettings()
