import httpx
from app.config import settings
from fastapi import HTTPException
from app.app.common import auth, headers, ATTRIBUTE_MAPPING
from app.utils.helpers import structure_objects
from urllib.parse import quote

async def get_objects_in_schema(schema_id: str, object_type: str | None, fields: list[str] | None = None):
    """
    Получает список объектов из указанной схемы с возможностью фильтрации по типу и выборки полей.

    Параметры:
        - schema_id (str): Идентификатор схемы объектов.
        - object_type_id (str | None): Идентификатор типа объекта (если передан, фильтрует объекты по типу).
        - fields (list[str] | None): Список полей для вывода (например, ['Key', 'type']).
    """

    # Базовый URL
    url = f"{settings.jira_base_url}/rest/insight/1.0/iql/objects?objectSchemaId={schema_id}&resultPerPage=180&start=86"
    print(object_type)
    if object_type:
        iql_query = f'objectType = "{object_type}"'
        encoded_iql_query = quote(iql_query)  # Кодируем кириллические символы
        url += f"&iql={encoded_iql_query}"

    # Добавляем выборку нужных полей в URL
    if fields:
        fields_param = ",".join(fields)
        url += f"&fields={fields_param}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth, headers=headers)
        print(response.json())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Ошибка выполнения IQL запроса: {response.status_code}")

        return response.json()