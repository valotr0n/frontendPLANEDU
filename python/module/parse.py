import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# Ссылка на учебный план ДГТУ
url = 'https://edu.donstu.ru/Plans/Plan.aspx?id=50288'

response = requests.get(url)

if response.status_code == 200:
    # Получаем всю HTML страничку
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все ссылки
    aLinks = soup.find_all('a', class_='aLink')

    # Найдём все ссылки на РПД
    for a_tag in aLinks:


        if "РПД" in a_tag.get_text():
            filename = a_tag.find_parent().find_parent().find(class_="dxgv dx-al").get_text()
            file_url = a_tag['href']

            if not file_url.startswith('http'):
                file_url = os.path.join(url, file_url)

            # Пытаемся скачать РПД
            print(file_url, filename)
            if filename == 'Математический анализ':
                try:
                    # Выполняем GET-запрос
                    response = requests.get(file_url)
                    response.raise_for_status()

                    # Сохраняем содержимое в файл
                    with open(f"{filename}.pdf", "wb") as file:
                        file.write(response.content)

                    print(f"Файл успешно сохранен как '{filename}'")

                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при загрузке файла: {e}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")