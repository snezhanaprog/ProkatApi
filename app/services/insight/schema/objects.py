import httpx
from fastapi import HTTPException
from urllib.parse import quote
from app.config import settings
from app.app.common import auth, headers
from typing import Optional

async def get_objects_in_schema(schema_id: str, object_type: Optional[str] = None):
    """
    Получает список объектов из указанной схемы с возможностью фильтрации по типу.

    Параметры:
        - schema_id (str): Идентификатор схемы объектов.
        - object_type (str | None): Название типа объекта (если передан, фильтрует объекты по типу).
    """

    # Базовый URL
    url = f"{settings.jira_base_url}/rest/insight/1.0/iql/objects?objectSchemaId={schema_id}&resultPerPage=180&start=0"

    # Фильтрация по типу объекта
    if object_type:
        iql_query = f'objectType = "{object_type}"'
        encoded_iql_query = quote(iql_query)  # Кодируем русские символы
        url += f"&iql={encoded_iql_query}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Ошибка выполнения IQL запроса: {response.status_code}")

        data = response.json()

        # Проверяем, есть ли объект "objectEntries" в ответе API
        if "objectEntries" not in data:
            raise HTTPException(status_code=500, detail="Отсутствует ключ 'objectEntries' в ответе API")

        objects = data["objectEntries"]

        # Формируем список с нужными полями: ключ, название, категория (тип объекта)
        filtered_objects = []
        for obj in objects:
            filtered_objects.append({
                "objectKey": obj.get("objectKey"),
                "name": obj.get("name") or obj.get("label"),  # Название может быть в "name" или "label"
                "category": obj.get("objectType", {}).get("name"),  # Достаем имя типа объекта
                "image": obj.get("avatar", {}).get("url48")
            })

        return filtered_objects