from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from module.main import AIModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Инициализация FastAPI
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


@app.post("/chat/")
async def chat(input_data: UserInput):
    """
    Обрабатывает пользовательский ввод через POST-запрос и возвращает ответ от модели.
    """
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


@app.post("/reset/")
async def reset_history():
    """
    Сбрасывает историю чата.
    """
    ai_model.reset_history()
    return {"message": "История чата сброшена."}
