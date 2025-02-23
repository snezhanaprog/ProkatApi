from pydantic_settings import BaseSettings
import httpx
from fastapi import FastAPI

class Settings(BaseSettings):
    jira_base_url: str
    jira_login: str
    jira_password: str

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI()
