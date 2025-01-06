import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/")
async def webhook(request: Request):
    try:
        json_data = await request.json()
        return JSONResponse(content={"status": 200, "message": "ok"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": 500, "message": str(e)}, status_code=500)

async def start_polling():
    bot = Bot(token=os.environ['TG_TOKEN'])
    dp = Dispatcher()
    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True, text="🤔"))

    def is_api_group(chat_id):
        return chat_id == os.environ['TG_ADMIN']

    @dp.message_handler(CommandStart())
    async def start(message: types.Message):
        await message.answer('hi!')

    await dp.start_polling(bot)

    @bot.message_handler(content_types=["text"])
    def foo(message):
        if is_api_group(str(message.chat.id)):
            bot.send_message(message.chat.id, 'ha-ha')

    

async def run_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=5400, log_level="warning", access_log=False)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(start_polling(), run_fastapi())

# for some reasons in this specific task we need poll while we have active endpoint on port
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped manually.")