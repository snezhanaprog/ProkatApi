import httpx
from app.config import settings
from fastapi import HTTPException
from app.app.common import auth, headers, ATTRIBUTE_MAPPING

async def get_objects_in_schema(schema_id: str):
    """
    Получает список объектов из указанной схемы.
    
    Если параметр search задан (например, часть названия или категория),
    формируется IQL-запрос для поиска по полям Name и Category.
    Если search пустой, возвращаются все объекты указанной схемы.
    """

    url = f"{settings.jira_base_url}/rest/insight/1.0/iql/objects?objectSchemaId={schema_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth, headers=headers)
        if response.status_code == 200:
            # Обычно объекты возвращаются в ключе 'objectEntries'.
            # Если структура отличается, адаптируйте обработку JSON.
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Ошибка выполнения IQL запроса: {response.status_code}")
        