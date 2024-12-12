from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent
from langchain.tools import tool
from langchain.llms import BaseLLM
from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentType
import sys
from schemes import template
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import compile_system_prompt
import asyncio

config = RunnableConfig(max_concurrency=10)
 
#TODO
system_prompt = compile_system_prompt("")

sear = SearxSearchWrapper(searx_host="http://localhost:8080")









@tool
def search_tool(InputQuery:str):
    """Используется для поиска информации и учебных материалов. Возвращать links"""
    results = sear.results(
        query = InputQuery,
        query_suffix = "!duckduckgo", #duckduckgo
        num_results=4,
        categories=["general"],
        language="ru-RU"

    )
    formatted_results = [{"snippet": result.get("snippet"), "title": result.get("title", "Без названия"), "link": result.get("link", "Ссылка отсутствует")} for result in results]
    return formatted_results

class AIModel:

    def __init__(self, model_name="llama3.1:8b-instruct-q5_K_S", temperature=1, top_k=10, base_url="http://localhost:11434"):
        self.model = ChatOllama(
            model=model_name,
            temperature=temperature,
            top_k=top_k,
            base_url=base_url  # Указываем URL сервера Ollama
        )
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
        self.chat_history = []
        self.agent = create_agent(self.model)
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
            result.append(chunk.content)
            yield chunk # Отправка данных по частям
        full_ai_response = ''.join(result)
        await self.save_system_message(full_ai_response)


    # Для агента и поиска информации в инете
    async def tool_process_message(self, user_input: str):
        self.chat_history.append(HumanMessage(content=user_input))
        messages = [self.system_message_prompt] + self.chat_history

        inputs = {"messages": [("user", user_input)]}
        async for chunk in self.agent.astream(inputs, config=config):
            try:
                yield chunk.get("agent").get("messages")[0].content.replace("\n", "/n")
                full_ai_response = ''.join(chunk.get("agent").get("messages")[0].content)
            except AttributeError:
                pass
        await self.save_system_message(full_ai_response)

    async def save_system_message(self, system_message: str):
        self.chat_history.append(AIMessage(system_message))

    def get_history(self):
        return self.chat_history

    def set_history(self, new_history):
        self.chat_history = new_history
        return self.chat_history
    


prompt = """ Ты ассистент который помогает студентам находить полезные учебные ресурсы.
Отвечай в виде.
      [Название ресурса]
      [Ссылка на ресурс]
      [Краткое описание ресурса]
"""

def create_agent(model: BaseLLM):
    tools = [search_tool]  # Добавляем инструменты
    agent = create_react_agent(model, tools, state_modifier=prompt)
    return agent


    

async def main():
    ai_model = AIModel()
    # Пример запроса
    user_query = "Паша Техник. Треки"
    async for response in ai_model.tool_process_message(user_query):
        print(response)
  
    # Пример запроса
    # user_query = "Три шага для изучения машинного обучения"
    # response = ai_model.process_message(user_query)

    # async for chunks in response:
    #     print(chunks.content.replace("\n", "/n"))
    #     break

if __name__ == "__main__":
    asyncio.run(main())