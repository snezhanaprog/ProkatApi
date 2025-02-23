def shorten_json(data: dict) -> dict:
    """
    Извлекает из длинного JSON с данными объекта следующие поля:
      - Key
      - Name
      - Created
      - Updated
      - Статус
      - Стоимость аренды в 1 час
      - Тип (в данном случае "Категория" – имя типа объекта)
      - Возраст
      - Цвет
      - Производитель
      - url_image (путь к картинке объекта)
    """
    result = {}

    # Верхнеуровневые поля
    result["Key"] = data.get("objectKey", "").strip()
    result["Name"] = data.get("name", "").strip()

    # Добавляем поле "Категория" (тип объекта)
    result["Категория"] = data.get("objectType", {}).get("name", "").strip()

    # Добавляем URL изображения из поля "avatar"
    # Здесь используем url144, можно выбрать другой размер по необходимости
    result["url_image"] = data.get("avatar", {}).get("url144", "").strip()

    # Обходим список атрибутов
    for attribute in data.get("attributes", []):
        attr_info = attribute.get("objectTypeAttribute", {})
        attr_name = attr_info.get("name", "").strip()
        values = attribute.get("objectAttributeValues", [])
        if not values:
            continue

        # Используем displayValue, если он есть, иначе value
        value = values[0].get("displayValue") or values[0].get("value", "")
        value = value.strip()

        if attr_name == "Created":
            result["Created"] = value
        elif attr_name == "Updated":
            result["Updated"] = value
        elif attr_name == "Статус":
            # Если значение представлено ссылкой, берем name из referencedObject
            if "referencedObject" in values[0]:
                result["Статус"] = values[0]["referencedObject"].get("name", "").strip()
            else:
                result["Статус"] = value
        elif attr_name == "Стоимость аренды в 1 час":
            result["Стоимость аренды в 1 час"] = value
        elif attr_name == "Тип":
            result["Тип"] = value
        elif attr_name == "Возраст":
            result["Возраст"] = value
        elif attr_name == "Цвет":
            result["Цвет"] = value
        elif attr_name == "Производитель":
            result["Производитель"] = value

    return result
