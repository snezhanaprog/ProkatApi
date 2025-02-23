from fastapi import FastAPI
from app.routers import jira

app = FastAPI(title="Jira Integration", version="1.0.0")

app.include_router(jira.router, prefix="/jira", tags=["Jira"])