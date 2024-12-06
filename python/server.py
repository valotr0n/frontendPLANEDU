from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.main import AIModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
from langchain_core.messages import HumanMessage, AIMessage
from database.database import get_faculties_db, get_roadmaps_db
app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)

# Инициализация модели
ai_model = AIModel()



#Стримовая версия 
async def stream_response(message: str):
    try:
        # Получаем потоковый ответ от модели
        async for chunk in ai_model.process_message(message):
            yield f"data: {chunk}\n\n"  # SSE формат данных
    except Exception as e:
        yield f"data: [Error] {str(e)}\n\n"


class UserInput(BaseModel):
    message: str

class HistoryItem(BaseModel):
    content: str
    additional_kwargs: dict
    response_metadata: dict
    type: str
    name: Optional[str] = None
    id: Optional[str] = None
    example: bool
    tool_calls: Optional[List] = None
    invalid_tool_calls: Optional[List] = None
    usage_metadata: Optional[dict] = None


class History(BaseModel):
    history: List[HistoryItem]


### API ДЛЯ НЕЙРОНКИ ##

#Обрабатывает пользовательский ввод через POST-запрос и возвращает ответ от модели.
@app.post("/chat/")
async def chat(input_data: UserInput):
    try:
        response = await ai_model.process_message(input_data.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Стримовый ендпоинт
@app.get("/chat-stream/")
async def chat_stream(message: str):
    return StreamingResponse(
        stream_response(message),
        media_type="text/event-stream"
    )

# Очистка памяти
@app.post("/reset/")
async def reset_history():
    ai_model.reset_history()
    return {"message": "История чата сброшена."}


@app.get("/get_history/")
async def get_history():
    history = ai_model.get_history()
    return  {"history": history}

@app.post("/set_history/")
async def set_history(history:History):
    history_list = []
    for item in history.history:
        if item.type == "human":
            history_list.append(HumanMessage(item.content))
        elif item.type == "ai":
            history_list.append(AIMessage(item.content))
    new_history = ai_model.set_history(history_list)
    return {"history": history_list} # new_history



### API ДЛЯ БАЗЫ ДАННЫХ ##
@app.get("/api/faculties/")
def get_faculties():
    data = get_faculties_db()
    return {"data": data}

@app.get("/api/roadmaps/")
def get_roadmaps():
    data = get_roadmaps_db("TODO")
    return {"data": data}