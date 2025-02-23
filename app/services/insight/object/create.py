import httpx
from app.config import settings
from app.app.common import auth, headers, ATTRIBUTE_MAPPING

async def create_object(object_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{settings.jira_base_url}/rest/insight/1.0/object/create',
            auth=auth,
            json=object_data,
            headers=headers
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f'Failed to create object: {response.status_code}')