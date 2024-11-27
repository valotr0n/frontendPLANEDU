import PyPDF2

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

def parse_rpd(text):
    data = {}
    sections = (text.split("Контрольные вопросы и задания")[1].split("5.2. Темы письменных работ")[0])
    if sections.split('Раздел')[1:]:
        print(sections.split('Раздел')[1:])
    else:
        print(sections)
    return data

if __name__ == "__main__":
    file_path = "Математический анализ.pdf"
    text = extract_text_from_pdf(file_path)
    if text:
        parsed_data = parse_rpd(text)

