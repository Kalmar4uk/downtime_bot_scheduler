import os

import nest_asyncio
import sentry_sdk
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.constants import TOKEN
from bot.scheduler.request_downtime import get_downtime

load_dotenv()
nest_asyncio.apply()

app = ApplicationBuilder().token(TOKEN).build()

sentry_sdk.init(os.getenv("DSN"))


async def start() -> None:
    """Главная функция запусков"""
    await get_downtime(app=app)

    try:
        await app.run_polling()
    except (KeyboardInterrupt, RuntimeError):
        print("Остановились")
