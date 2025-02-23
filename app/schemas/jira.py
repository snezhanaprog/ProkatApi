from pydantic import BaseModel

class JiraIssue(BaseModel):
    project_key: str
    summary: str
    description: str
    issuetype: str