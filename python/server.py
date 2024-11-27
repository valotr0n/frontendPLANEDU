# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import JSONResponse
# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel

# app = FastAPI()



# origins = ["*"]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
#     allow_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
# )


# class Item(BaseModel):
#     message: str

# @app.post("/api/message/")
# async def create_item(request: Request):
#     data = await request.json()
#     text_content = data.get("text_content", "")
#     response = fz.getUserMessage(text_content)
#     return JSONResponse(content={"response": response})






# from fastapi import FastAPI, WebSocket
# from fastapi.responses import JSONResponse
# from module.test import process_message

# app = FastAPI()

# @app.post("/chat")
# async def chat_endpoint(input_message: str):
#     """
#     Обрабатывает POST-запрос с текстом сообщения пользователя.
#     Возвращает полный ответ модели (не потоковый).
#     """
#     try:
#         response_generator = process_message(input_message)

#         # Собираем все данные из асинхронного генератора
#         response = "".join([chunk async for chunk in response_generator])
#         return JSONResponse(content={"response": response})
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)


# @app.websocket("/ws/chat")
# async def websocket_chat_endpoint(websocket: WebSocket):
#     """
#     Обрабатывает WebSocket-запросы для потокового взаимодействия с моделью.
#     """
#     await websocket.accept()
#     try:
#         while True:
#             user_input = await websocket.receive_text()
#             if user_input.lower() in ['quit', 'exit']:
#                 await websocket.close()
#                 break

#             response_stream = process_message(user_input)
#             async for chunk in response_stream:
#                 await websocket.send_text(chunk)
#             await websocket.send_text("[END]")  # Отметка конца потока
#     except Exception as e:
#         await websocket.send_text(f"Error: {str(e)}")
#         await websocket.close()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from module.test import AIModel
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
