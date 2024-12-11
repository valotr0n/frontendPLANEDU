from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent
from langchain.tools import tool
from langchain.llms import BaseLLM
from langchain.agents import AgentType
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import compile_system_prompt
import asyncio

config = RunnableConfig(max_concurrency=10)
 
#TODO
system_prompt = compile_system_prompt("")

sear = SearxSearchWrapper(searx_host="http://searxng:8080")

@tool
def search_tool(InputQuery:str):
    """Используется для поиска информации через Searx."""
    results = sear.results(
        query = InputQuery,
        query_suffix = "!duckduckgo", #duckduckgo
        num_results=5,
        categories=["general"],
        language="ru-RU"

    )
    return results

class AIModel:
    def __init__(self, model_name="llama3.1:8b-instruct-q5_K_S", temperature=1, top_k=10, base_url="http://ollama:11434"):
        self.model = OllamaLLM(
            model=model_name,
            temperature=temperature,
            top_k=top_k,
            base_url=base_url  # Указываем URL сервера Ollama
        )
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
        self.chat_history = []

    def reset_history(self):
        self.chat_history = []

    async def process_message(self, user_input: str):
        HumanMessagePromptTemplate.from_template(user_input)
        self.chat_history.append(HumanMessage(content=user_input))
        messages = [self.system_message_prompt] + self.chat_history
        prompt = ChatPromptTemplate.from_messages(messages).format_prompt()

        async_stream = (self.model.astream(input=prompt.to_string(), config=config))
        result = []
        async for chunk in async_stream:
            result.append(chunk)
            yield chunk  # Отправка данных по частям
        full_ai_response = ''.join(result)
        await self.save_system_message(full_ai_response)


    async def save_system_message(self, system_message: str):
        self.chat_history.append(AIMessage(system_message))

    def get_history(self):
        return self.chat_history

    def set_history(self, new_history):
        self.chat_history = new_history
        return self.chat_history
    

def create_agent(model: BaseLLM):
    tools = [search_tool]  # Добавляем инструменты
    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent

async def main():
    ai_model = AIModel()
    agent = create_agent(ai_model.model)

    # Пример запроса
    user_query = "Учебные материалы по Первый замечательный предел. Матанализ."
    response = await agent.arun(user_query)
    print("Ответ от агента:", response)


if __name__ == "__main__":
    asyncio.run(main())