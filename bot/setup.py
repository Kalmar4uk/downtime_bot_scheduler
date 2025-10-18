import os

import nest_asyncio
import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.ext import ApplicationBuilder

from bot.constants import TOKEN
from bot.scheduler.request_downtime import get_downtime

nest_asyncio.apply()

app = ApplicationBuilder().token(TOKEN).build()
scheduler = AsyncIOScheduler()

sentry_sdk.init(os.getenv("DSN"))


async def setup_scheduler() -> None:
    """Запуск планировщика"""
    try:
        scheduler.add_job(
            get_downtime,
            CronTrigger(hour=14, minute=9, second=50),
            id="get_downtime",
            timezone="Europe/Moscow",
            kwargs={"app": app}
        )
        scheduler.start()
    except Exception as e:
        print(f"Ошибка при запуске планировщика: {e}")


async def start() -> None:
    """Главная функция запусков"""
    await setup_scheduler()

    try:
        await app.run_polling()
    except (KeyboardInterrupt, RuntimeError):
        print("Остановились")
