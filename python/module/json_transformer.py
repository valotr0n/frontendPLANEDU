import json

# Исходные данные
data = [
    "1. Функции. Пределы. Непрерывность функций.",
    "1.2 Числовые множества. Определение и способы задания функции /Пр/",
    "1.5 Вычисление пределов последовательностей. Раскрытие неопределенностей. /Пр/",
    "1.8 Вычисление пределов функций. Сравнение бесконечно малых функций /Пр/",
    "1.11 Исследование функции на непрерывность. Классификация точек разрыва. Контрольная работа № 1 «Предел функции» /Пр/"
]
#TODO
# Функция для создания иерархии
def create_hierarchy(data):
    root = {
        "id": "vmo",
        "name": "Математическое образование",
        "type": "section",
        "optional": False,
        "children": []
    }
    
    current_level = root["children"]
    
    for item in data:
        parts = item.split()
        level = int(parts[0].split('.')[0])
        name = ' '.join(parts[1:])
        
        # Убираем "/Пр/" из названия, если оно есть
        name = name.replace('/Пр/', '').strip()
        
        # Создаем словарь для текущего элемента
        node = {
            "id": name.split(" ")[0].lower().replace(' ', '-').replace(".", ''),
            "name": name,
            "children": []
        }
        
        # Если уровень меньше текущего, поднимаемся наверх
        while len(current_level) < level - 1:
            current_level = current_level[-1]["children"]
        
        # Добавляем текущий элемент в текущий уровень
        current_level.append(node)
        
        # Переходим на следующий уровень
        current_level = node["children"]
    
    return root

# Создаем иерархию
hierarchy = create_hierarchy(data)

# Выводим результат в формате JSON
print(json.dumps(hierarchy, ensure_ascii=False, indent=2))