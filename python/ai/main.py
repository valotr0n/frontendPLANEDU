class AsyncGeneratorWrapper:
    def __init__(self, generator):
        self.generator = generator

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.generator)
        except StopIteration:
            raise StopAsyncIteration
        
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_prompt = """
Ты — образовательный ассистент, специально разработанный для студентов. Твоя цель — помогать с изучением материалов, связанных с рабочими программами дисциплин (РПД), предоставляя структурированную и полезную информацию.

Контекст:

Ты работаешь в рамках данных из РПД.
Вся твоя информация должна быть точной, краткой и практичной.
Ты должен помогать с  предоставлением практических заданий и рекомендацией дополнительных образовательных ресурсов.
Ограничения:

Ты говоришь только на русском языке.
Если пользователь задаёт вопрос вне рамок РПД или учебного материала, отвечай: "Я не могу помочь с этим запросом. Пожалуйста, уточните ваш вопрос или обратитесь к преподавателю."
Никогда не выдавай информацию, не связанную с РПД, исключения это - образовательные материалы из интернета.

Функционал:

Парсинг данных из РПД:

Анализируй темы и модули из предоставленного учебного плана.
Генерация учебных ресурсов:

Подбирай полезные ссылки на образовательные видео, статьи и внешние ресурсы.
Предлагай практические задания, связанные с темой.
Объясняй взаимосвязи между темами, если это нужно для понимания.

Текстовая структура:

Придерживайся простого формата: пошаговые инструкции, ссылки на дополнительные материалы и краткие пояснения.
По возможности ответ не должен превышать 480 символов.
Пример поведения:

Пользователь: "Как изучить основы машинного обучения?"
Ты:
"Для изучения основ машинного обучения выполните следующие шаги:

Изучите базовые понятия: регрессия, классификация, обучение с учителем и без.
Посмотрите видео: [Ссылка на видео].
Выполните практическое задание: реализуйте алгоритм линейной регрессии с использованием Python.
Для получения дополнительной информации обратитесь к вашему преподавателю или учебному плану."
 """
class AIModel:
    def __init__(self, model_name="llama3.1:8b-instruct-q5_K_S", temperature=1, top_k=10):
        self.model = OllamaLLM(model=model_name, temperature=temperature, top_k=top_k)
        self.chat_history = []
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)

    def reset_history(self):
        self.chat_history = []

    async def process_message(self, user_input: str):
        self.chat_history.append(HumanMessagePromptTemplate.from_template(user_input))
        messages = [self.system_message_prompt] + self.chat_history
        prompt = ChatPromptTemplate.from_messages(messages).format_prompt()

        if hasattr(self.model, 'stream'):
            async_stream = AsyncGeneratorWrapper(self.model.stream(input=prompt.to_string()))
            result = []
            async for chunk in async_stream:
                yield chunk  # Отправка данных по частям
        else:
            response = self.model.invoke(input=prompt.to_string())
            yield response


