import PyPDF2
import re
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        return f"Ошибка при обработке файла: {e}"


# TODO
def parse_rpd(text):
    data = {}
    sections = (text.split("4. СТРУКТУРА И СОДЕРЖАНИЕ ДИСЦИПЛИНЫ (МОДУЛЯ)")[1].split("5. ОЦЕНОЧНЫЕ МАТЕРИАЛЫ (ОЦЕНОЧНЫЕ СРЕДСТВА)")[0])
    if sections.split('Раздел')[1:]:
        s = ''.join(sections.split('Раздел')[1:])
        # print(s.split("\n"))
        result = []
        for z in s.split("\n"):
            if "ОПК" in z or "/Ср/"  in  z or "/ИКР/" in z:
                pass
            else:
                cleaned_line = re.sub(r'\s*Л\d+\.\d+\s*', '', z).strip()
                result.extend(cleaned_line.split("\n"))
                print(cleaned_line)
if __name__ == "__main__":
    file_path = "Математический анализ.pdf"
    text = extract_text_from_pdf(file_path)
    if text:
        parsed_data = parse_rpd(text)

## import PyPDF2
# import re
# def extract_text_from_pdf(file_path):
#     try:
#         with open(file_path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             text = ''
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#             return text
#     except Exception as e:
#         return f"Ошибка при обработке файла: {e}"

# def parse_rpd(text):
#     data = (text.split("СТРУКТУРА И СОДЕРЖАНИЕ ДИСЦИПЛИНЫ (МОДУЛЯ)")[1].split("Раздел 2. Дифференциальное исчисление функции одной переменной и его приложения")[0])
#     # if sections.split('Раздел')[1:]:
#     #     print(sections.split('Раздел')[1:])
#     # else:
#     #     print(sections)
#     print(extract_topics_and_sections(data))



# def extract_topics_and_sections(text):
#     # Регулярные выражения для поиска разделов и тем
#     section_pattern = re.compile(r"Раздел\s+\d+\.\s+.*")
#     topic_pattern = re.compile(r"\d+\.\d+\s+.*")

#     sections_and_topics = []

#     # Разделить текст на строки
#     lines = text.splitlines()
#     for line in lines:
#         line = line.strip()
#         # Проверяем, является ли строка разделом или темой
#         if section_pattern.match(line) or topic_pattern.match(line):
#             sections_and_topics.append(line)

#     return "\n".join(sections_and_topics)

# if __name__ == "__main__":
#     file_path = "Математический анализ.pdf"
#     text = extract_text_from_pdf(file_path)
#     if text:
#         parsed_data = parse_rpd(text)