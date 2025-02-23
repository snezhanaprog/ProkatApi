import httpx
from app.config import settings
from fastapi import HTTPException
from app.utils.helpers import shorten_json
from app.app.common import auth, headers, ATTRIBUTE_MAPPING

async def get_object_details(schema_id: str, object_id: str):
    url = f"{settings.jira_base_url}/rest/insight/1.0/object/{object_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth, headers=headers)
        if response.status_code == 200:
            object_data = response.json()
            if str(object_data.get('objectType', {}).get('objectSchemaId')) != schema_id:
                raise HTTPException(status_code=404,
                                    detail=f"Объект с id {object_id} не найден в схеме {schema_id}")
            return shorten_json(object_data)
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Не удалось получить объект: {response.status_code}")