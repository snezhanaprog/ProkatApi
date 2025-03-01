from fastapi import APIRouter
from typing import List, Dict, Any
from app.config import settings
from app.schemas.jira import JiraIssue
from fastapi import HTTPException, Query
from app.services.insight.object.create import create_object
from app.services.insight.object.retrieve import get_object_details
from app.services.insight.object.update import update_object_details
from typing import Optional
from app.services.insight.schema.list import get_object_schemas
from app.services.insight.schema.objects import get_objects_in_schema
from app.services.insight.schema.objecttypes import get_objecttypes_schema

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "Welcome to Jira Integration API!",
        "jira_base_url": settings.jira_base_url,
        "jira_login": settings.jira_login,
    }

@router.get("/schemas", response_model=Dict[str, Any])
async def list_schemas():
    return await get_object_schemas()

@router.get("/schemas/{schema_id}/objects")
async def list_objects(schema_id: str, object_type: Optional[str] = None):
    return await get_objects_in_schema(schema_id, object_type)

@router.get("/schemas/{schema_id}/objecttypes")
async def list_objectstypes(schema_id: str):
    return await get_objecttypes_schema(schema_id)

@router.post("/objects", response_model=Dict[str, Any])
async def create_assets_object(object_data: dict):
    return await create_object(object_data)

@router.post("/{schema_id}/objects/{object_id}")
async def object_details(schema_id, object_id):
    return await get_object_details(schema_id, object_id)

@router.put("/{schema_id}/objects/{object_id}/update")
async def object_update(schema_id, object_id, updated_fields: dict):
    return await update_object_details(schema_id, object_id, updated_fields)
  