import httpx
from app.config import settings
from app.app.common import auth, headers, ATTRIBUTE_MAPPING

async def get_objecttypes_schema(schema_id:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.jira_base_url}/rest/insight/1.0/objectschema/{schema_id}/objecttypes',
            auth=auth, 
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'failed to fetch objecttypes schemas: {response.status_code}')