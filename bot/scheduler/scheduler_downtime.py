from datetime import datetime, timedelta

import requests
from telegram.ext import ApplicationBuilder

from bot import setup
from bot.constants import (CHAT_ID, DATE_FORMAT, HEADERS, NEWSLETTER,
                           TIME_FORMAT, URL, MY_CHAT)
from bot.exceptions import ErrorSendMessage, ErrorStartSchedule
from bot.utils import Downtime


async def get_downtime(app: ApplicationBuilder) -> None:
    try:
        downtime: dict = requests.get(URL, headers=HEADERS).json()  # Api отдает массив объектов, надо будет переписать на случай, если объектов > 1
    except Exception as e:
        await send_error(
            app=app,
            error=(
                f"Возникла ошибка при отправке "
                f"запроса get api/downtime: {str(e)}")
        )

    if downtime:
        # message = [Downtime.preparation(data=data) for data in downtime]
        message = Downtime.preparation(data=downtime[0])
        try:
            await send_message(data=message, app=app)
            await scheduler_reminder(app=app, data=message)
        except ErrorStartSchedule as e:
            await send_error(app=app, error=str(e))
        except ErrorSendMessage as e:
            await send_error(app=app, error=str(e))


async def send_error(app: ApplicationBuilder, error: str):
    await app.bot.send_message(
            chat_id=MY_CHAT,
            text=error,
        )


async def scheduler_reminder(
        app: ApplicationBuilder,
        data: Downtime
) -> None:
    reminder_time: datetime = (
        data.start_downtime - timedelta(hours=1, minutes=30)
    )

    try:
        setup.scheduler.add_job(
            send_message,
            "date",
            run_date=reminder_time,
            id=f"reminder_{reminder_time}",
            kwargs={"data": data, "app": app, "reminder_time": reminder_time}
        )
    except Exception as e:
        raise ErrorStartSchedule(
            f"Возникла ошибка при запуске "
            f"планировщика второго напоминания: {str(e)}"
        )


async def send_message(
        data: Downtime,
        app: ApplicationBuilder,
        reminder_time: datetime | None = None
) -> None:
    try:
        text: str = (
            f"<b>{data.start_downtime.date().strftime(DATE_FORMAT)}</b>\n"
            f"С <b>{data.start_downtime.time().strftime(TIME_FORMAT)}</b> "
            f"По <b>{data.end_downtime.time().strftime(TIME_FORMAT)}</b>\n"
            f"Cервис: <b>{data.service}</b>\n"
            f"Будет произведено: <b>{data.description}</b>\n"
            f"Даунтайм согласован в рамках задачи: {data.link_task}\n"
            f"Ответственный со стороны ГСМАиЦП:\n"
            f"<b>{data.last_name} {data.first_name}</b>"
        )
    except Exception as e:
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения планировщика: {str(e)}"
        )

    if not reminder_time:
        news = f"{text}\n\n{NEWSLETTER.format('15:00')}"
    else:
        news = (
            f"{text}\n\n"
            f"{NEWSLETTER.format(reminder_time.time().strftime(TIME_FORMAT))}"
        )

    try:
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text=news,
            parse_mode="HTML"
        )
    except Exception as e:
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения планировщика: {str(e)}"
        )
