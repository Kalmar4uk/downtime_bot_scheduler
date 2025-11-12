from datetime import datetime, timedelta

import requests
from telegram.ext import ApplicationBuilder

from bot import setup
from bot.constants import (CHAT_ID, DATE_FORMAT, HEADERS, MY_CHAT, NEWSLETTER,
                           TIME_FORMAT, URL)
from bot.exceptions import ErrorSendMessage, ErrorStartSchedule
from bot.logs_settings import logger
from bot.utils import Downtime


async def get_downtime(app: ApplicationBuilder) -> None:
    date_downtime: datetime = datetime.now().date() + timedelta(days=1)

    try:
        logger.info("Отправили запрос на получение плановых работ")
        downtime: dict = requests.get(
            URL.format(date_downtime, date_downtime),
            headers=HEADERS
        ).json()
    except Exception as e:
        logger.error(f"Возникла ошибка при обработке запроса: {str(e)}")
        await send_error(
            app=app,
            error=(
                f"Возникла ошибка при отправке "
                f"запроса get api/downtime: {str(e)}")
        )

    if downtime:
        logger.info("Получили данные о плановых работах")
        message = Downtime.preparation(data=downtime[0])
        logger.info("Проверили время старта")
        if (
            message.start_downtime.date() == (
                datetime.now().date() + timedelta(days=1)
            )
        ):
            try:
                logger.info("Отправили сообщение в чат")
                await send_message(data=message, app=app)

                logger.info("Отправили данные для второго уведомления")
                await scheduler_reminder(app=app, data=message)
            except Exception as e:
                logger.error(
                    f"Возникла ошибка при отправке сообщения "
                    f"или планирования второго уведомления: {str(e)}"
                )
                await send_error(app=app, error=str(e))


async def send_error(app: ApplicationBuilder, error: str):
    logger.info("Отправили сообщение об ошибке в чат администратору")
    await app.bot.send_message(
            chat_id=MY_CHAT,
            text=error,
        )


async def scheduler_reminder(
        app: ApplicationBuilder,
        data: Downtime
) -> None:
    logger.info("Рассчитали время повторого уведомления")
    reminder_time: datetime = (
        data.start_downtime - timedelta(hours=1, minutes=30)
    )

    try:
        logger.info("Запустили планировщик повторного уведомления")
        setup.scheduler.add_job(
            send_message,
            "date",
            run_date=reminder_time,
            id=f"reminder_{reminder_time}",
            kwargs={"data": data, "app": app, "reminder_time": reminder_time}
        )
    except Exception as e:
        logger.error(
            f"Возникла ошибка при планировании "
            f"повторного уведомления: {str(e)}"
        )
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
        logger.info("Подготовили текст сообщения для уведомления")
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
        logger.error(f"Возникла ошибка при отправке сообщения планировщика: {str(e)}")
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
        logger.info("Отправили напоминание в чат")
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text=news,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(
            f"Возникла ошибка при отправке сообщения планировщика: {str(e)}"
        )
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения планировщика: {str(e)}"
        )
