from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import compile_system_prompt

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


#TODO
system_prompt = compile_system_prompt("")

class AIModel:
    def __init__(self, model_name="llama3.1:8b-instruct-q5_K_S", temperature=1, top_k=10):
        self.model = OllamaLLM(model=model_name, temperature=temperature, top_k=top_k)
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
        self.chat_history = []

    def reset_history(self):
        self.chat_history = []

    async def process_message(self, user_input: str):
        HumanMessagePromptTemplate.from_template(user_input)
        self.chat_history.append(HumanMessage(content=user_input))
        messages = [self.system_message_prompt] + self.chat_history
        prompt = ChatPromptTemplate.from_messages(messages).format_prompt()

        
        async_stream = AsyncGeneratorWrapper(self.model.stream(input=prompt.to_string()))
        result = []
        async for chunk in async_stream:
            result.append(chunk)
            yield chunk  # Отправка данных по частям
        full_ai_response = ''.join(result)
        self.save_system_message(full_ai_response)


    def save_system_message(self, system_message: str):
        self.chat_history.append(AIMessage(system_message))

    def get_history(self):
        return self.chat_history

    def set_history(self, new_history):
        self.chat_history = new_history
        return self.chat_history
        