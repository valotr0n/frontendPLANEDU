# llama3.1:8b-instruct-q5_K_S
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.memory import ConversationBufferMemory
from config import system_prompt

system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

model = OllamaLLM(model="llama3.1:8b-instruct-q5_K_S")

user_input = "Привет. Как сварить борщ?"

prompt = chat_prompt.format_prompt(input=user_input)
formatted_prompt = prompt.to_string()
result = model.invoke(input=formatted_prompt)
print(result)

print(system_prompt)