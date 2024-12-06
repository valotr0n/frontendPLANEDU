import json
import random as rnd
from pdfread import zombie
# Исходные данные
data = zombie("Математический анализ")
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
        new_name = name.replace('/Пр/', '').strip()
        
        # Создаем словарь для текущего элемента
        node = {
            "id": new_name.split(" ")[0].lower().replace(' ', '-').replace(".", '') + str(rnd.randint(1,1000)),
            "name": new_name,
            "children": []
        }
        
        # Добавляем текущий элемент в текущий уровень
        current_level.append(node)

        if "/Пр/" not in name: 
            # Переходим на следующий уровень
            current_level = node["children"]
    
    return root

# Создаем иерархию
hierarchy = create_hierarchy(data)

# Выводим результат в формате JSON
print(json.dumps(hierarchy, ensure_ascii=False, indent=2))