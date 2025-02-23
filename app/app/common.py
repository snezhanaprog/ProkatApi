import httpx
from app.config import settings

auth = httpx.BasicAuth(settings.jira_login, settings.jira_password)
headers = {'Accept': "application/json"}

ATTRIBUTE_MAPPING = {
    "Key": 484,
    "Name": 485,
    "Статус": 827,
    "Стоимость аренды в 1 час": 828,
    "Тип": 952,
    "Возраст": 835,
    "Цвет": 829,
    "Производитель": 831,
}