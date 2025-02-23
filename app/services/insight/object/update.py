import httpx
from app.config import settings
from fastapi import HTTPException
from app.app.common import auth, headers, ATTRIBUTE_MAPPING

async def update_object_details(object_id: str, updated_fields: dict):
    attributes_payload = []
    for field, value in updated_fields.items():
        attribute_id = ATTRIBUTE_MAPPING.get(field)
        if not attribute_id:
            continue
        attributes_payload.append({
            "objectTypeAttributeId": attribute_id,
            "objectAttributeValues": [{"value": value}]
        })
    payload = {"attributes": attributes_payload}
    url = f"{settings.jira_base_url}/rest/insight/1.0/object/{object_id}"
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=payload, auth=auth, headers=headers)
        if response.status_code in (200, 204):
            return response.json() if response.content else {"detail": "Объект успешно обновлен"}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ошибка обновления объекта: {response.status_code}, {response.text}"
            )