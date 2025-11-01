import os

import nest_asyncio
import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.ext import ApplicationBuilder

from bot.bot_handlers.handlers import (error_handler, handlers_create_downtime,
                                       start_handler)
from bot.constants import MY_COMMANDS, TOKEN
from bot.exceptions import ErrorStartSchedule
from bot.scheduler.scheduler_downtime import get_downtime

nest_asyncio.apply()

app = ApplicationBuilder().token(TOKEN).build()
scheduler = AsyncIOScheduler()

sentry_sdk.init(os.getenv("DSN_BOT"))


async def setup_scheduler() -> None:
    """Запуск планировщика"""
    try:
        scheduler.add_job(
            get_downtime,
            CronTrigger(hour=11),
            id="get_downtime",
            timezone="Europe/Moscow",
            kwargs={"app": app}
        )
        scheduler.start()
    except Exception as e:
        raise ErrorStartSchedule(f"Ошибка при запуске планировщика: {str(e)}")


async def start() -> None:
    """Главная функция запусков"""
    await app.bot.set_my_commands(MY_COMMANDS)
    app.add_error_handler(error_handler)
    await setup_scheduler()
    await start_handler(app=app)
    await handlers_create_downtime(app=app)

    try:
        await app.run_polling()
    except (KeyboardInterrupt, RuntimeError):
        print("Остановились")
    except Exception as e:
        print(f"Возникла ошибка: {e}")
