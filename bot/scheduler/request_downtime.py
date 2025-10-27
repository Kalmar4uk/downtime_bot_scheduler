from datetime import datetime, timedelta

import requests
from telegram.ext import ApplicationBuilder

from bot import setup
from bot.constants import (CHAT_ID, DATE_FORMAT, HEADERS, NEWSLETTER,
                           TIME_FORMAT, URL)
from bot.utils import Downtime


async def get_downtime(app: ApplicationBuilder) -> None:
    downtime: dict = requests.get(URL, headers=HEADERS).json()  # Api отдает массив объектов, надо будет переписать на случай, если объектов > 1
    if downtime:
        # message = [Downtime.preparation(data=data) for data in downtime]
        message = Downtime.preparation(data=downtime[0])
        await send_message(data=message, app=app)
        await scheduler_reminder(app=app, data=message)


async def scheduler_reminder(
        app: ApplicationBuilder,
        data: Downtime
) -> None:
    reminder_time: datetime = data.start - timedelta(hours=1, minutes=30)

    setup.scheduler.add_job(
        send_message,
        "date",
        run_date=reminder_time,
        id=f"reminder_{reminder_time}",
        kwargs={"data": data, "app": app, "reminder_time": reminder_time}
    )


async def send_message(
        data: Downtime,
        app: ApplicationBuilder,
        reminder_time: datetime | None = None
) -> None:
    text: str = (
        f"<b>{data.start.date().strftime(DATE_FORMAT)}</b>\n"
        f"С <b>{data.start.time().strftime(TIME_FORMAT)}</b> "
        f"По <b>{data.end.time().strftime(TIME_FORMAT)}</b>\n"
        f"Cервис: <b>{data.service}</b>\n"
        f"Будет произведено: <b>{data.description}</b>\n"
        f"Даунтайм согласован в рамках задачи: {data.link}\n"
        f"Ответственный со стороны ГСМАиЦП:\n"
        f"<b>{data.last_name} {data.first_name}</b>"
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
        print(f"Возникла ошибка {e}")
