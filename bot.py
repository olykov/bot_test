import os
import asyncio
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.api_route("/", methods=["GET", "POST"])
async def handle_webhook(request: Request):
    if request.method == "GET":
        # Handle GET request
        return JSONResponse(content={"status": 200, "message": "ok"}, status_code=200)
    
    elif request.method == "POST":
        # Handle POST request
        try:
            json_data = await request.json()
            return JSONResponse(content={"status": 200, "message": "ok"}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"status": 500, "message": str(e)}, status_code=500)

async def start_polling():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    router = Router()
    dp.include_router(router)
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True, text="🤔"))

    def is_api_group(chat_id):
        return chat_id == os.environ['TG_ADMIN']

    @router.message(CommandStart())
    async def start(message: types.Message):
        print("start was called")
        await message.answer('hi!')

    @router.message()
    async def foo(message: types.Message):
        if is_api_group(str(message.chat.id)):
            print(f"text {message.text} received from {message.chat.id}")
            await message.answer('ha-ha')

    await dp.start_polling(bot)
    

async def run_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT")), log_level="warning", access_log=False)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(start_polling(), run_fastapi())

# for some reasons in this specific task we need poll while we have active endpoint on port
if __name__ == "__main__":
    try:
        BOT_TOKEN = os.getenv("TG_TOKEN")
        if not BOT_TOKEN or not os.getenv("TG_ADMIN"):
            raise ValueError("Bot token or TG_ADMIN aren't set. Please configure your environment.")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped manually.")