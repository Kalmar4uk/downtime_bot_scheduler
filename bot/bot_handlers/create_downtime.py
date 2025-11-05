import json
import re
from datetime import datetime, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler
from telegram_bot_calendar import DetailedTelegramCalendar

from bot.api.requests_to_backend import create_post_request
from bot.constants import PATTERN_LINK
from bot.decorators import check_type_chat, require_auth
from bot.exceptions import (ErrorRequestDowntime, ErrorSendMessage,
                            ErrorTransformDatetime)
from bot.logs_settings import logger
from bot.utils import (Downtime, generate_calendar, generate_hour,
                       generate_minute)


@check_type_chat
@require_auth
async def service_for_create_downtime(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Запущена функция добавления плановых работ")
    context.user_data["downtime"] = Downtime()
    try:
        logger.info("Отправили запрос названия сервиса")
        await update.message.reply_text(
            "Введи название сервиса или отправь /cancel для остановки"
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {str(e)}")

    return "SERVICE"


async def calendar_for_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Получение название сервиса"""
    logger.info("Получили название сервиса")
    downtime: Downtime = context.user_data.get("downtime")
    downtime.save_service_and_description(
        data=update.message.text.strip(),
        is_service=True
    )

    reply_markup = await generate_calendar()

    try:
        logger.info("Отправили календарь в чат")
        await update.message.reply_text(
            "Выбери дату или отправь /cancel для остановки",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )

    return "CALENDAR"


async def calendar_create(
        update: Update,
        context: CallbackContext
) -> int:
    """Работа с календарем"""
    result, key, _ = DetailedTelegramCalendar(
        locale="ru"
    ).process(
        update.callback_query.data
    )

    if not result and key:
        key = json.loads(key)
        reply_markup = InlineKeyboardMarkup(key["inline_keyboard"])

        try:
            await update.callback_query.edit_message_text(
                "Выбери дату или отправь /cancel для остановки:",
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )

    elif result:
        logger.info("Получили данные с календаря")
        downtime: Downtime = context.user_data.get("downtime")

        if not downtime.start_downtime:
            downtime.start_downtime = result
        else:
            downtime.end_downtime = result

        await update.callback_query.delete_message()

        reply_markup_hour = await generate_hour()

        try:
            logger.info("Отправили часы в чат")
            await update.callback_query.message.reply_text(
                "Выбери час или отправь /cancel для остановки",
                reply_markup=reply_markup_hour
            )
        except Exception as e:
            logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )

        return "HOUR"


async def hour_create(update: Update, context: CallbackContext) -> int:
    logger.info("Получили данные со времени (часы)")
    hour = update.callback_query
    context.user_data["hour"] = hour.data
    await hour.answer()
    await update.callback_query.delete_message()

    reply_markup = await generate_minute()

    try:
        logger.info("Отправили минуты в чат")
        await update.callback_query.message.reply_text(
            "Выбери минуты или отправь /cancel для остановки",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )

    return "MINUTE"


async def minute_create(update: Update, context: CallbackContext) -> int:
    logger.info("Получили данные со времени (минуты)")
    minute = update.callback_query
    await minute.answer()
    await update.callback_query.delete_message()

    hour: str = context.user_data.get("hour")
    downtime: Downtime = context.user_data.get("downtime")

    clock: time = time(int(hour), int(minute.data))
    try:
        if not context.user_data.get("minute"):
            downtime.start_downtime = datetime.combine(
                downtime.start_downtime, clock
            )
        else:
            downtime.end_downtime = datetime.combine(
                downtime.end_downtime, clock
            )
    except Exception as e:
        logger.error(f"Возникла ошибка при преобразовании даты: {str(e)}")
        await update.callback_query.message.reply_text(
            f"Возникла ошибка при преобразовании даты: {e}"
        )
        raise ErrorTransformDatetime(
            f"Возникла ошибка при преобразовании даты: {e}"
        )

    context.user_data["minute"] = minute.data

    if not context.user_data.get("date_end"):
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data="да"),
                InlineKeyboardButton("Нет", callback_data="нет")
            ]
        ]
        try:
            logger.info("Отправили запрос совпадения даты или нет")
            await update.callback_query.message.reply_text(
                "Дата окончания совпадает с датой начала работ ?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            logger.error(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {e}"
            )

        return "CHECK_DATE"

    try:
        logger.info("Отправили запрос ссылки в чат")
        await update.callback_query.message.reply_text(
            "Введи ссылку на задачу проведения работ"
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )

    return "LINK"


async def check_date(update: Update, context: CallbackContext) -> int:
    logger.info("Получили данные старта плановых работ (дата и время)")
    context.user_data["date_end"] = True
    check = update.callback_query
    await check.answer()

    if check.data == "да":
        downtime: Downtime = context.user_data.get("downtime")
        downtime.end_downtime = downtime.start_downtime.date()
        reply_markup_hour = await generate_hour()
        try:
            logger.info("Отправили запрос времени (часы) даты конца")
            await check.edit_message_text(
                "Выбери час или отправь /cancel для остановки",
                reply_markup=reply_markup_hour
            )
        except Exception as e:
            logger.error(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )

        return "HOUR"

    else:
        reply_markup = await generate_calendar()

        try:
            logger.info("Отправили календарь для даты окончания")
            await update.callback_query.edit_message_text(
                "Выбери дату или отправь /cancel для остановки",
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
            )

        return "CALENDAR"


async def link_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Получили ссылку")
    link = update.message.text.strip()
    if not re.match(PATTERN_LINK, link):
        try:
            logger.info(
                "Отправили предупреждение о некорректно введенной ссылки"
            )
            await update.message.reply_text(
                "Это не похоже на корректную ссылку на даунтайм.\n"
                "Нужна ссылка в формате:\n"
                "https://tracker.yandex.ru/DOWNTIME-XXXX\n\n"
            )
        except Exception as e:
            logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
            raise ErrorSendMessage(
                f"Возникла ошибка при отправке сообщения в чат: {e}"
            )
        return "LINK"
    downtime: Downtime = context.user_data.get("downtime")
    downtime.link_task = link

    try:
        logger.info("Отправили запрос на получение краткого описания")
        await update.message.reply_text("Введи краткое описание работ")
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )

    return "DESCRIPTION"


async def desctiption_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Получили краткое описание")
    downtime: Downtime = context.user_data.get("downtime")
    downtime.save_service_and_description(data=update.message.text.strip())
    try:
        logger.info("Отправили в чат все полученные данные")
        await update.message.reply_text(
            f"Введенные данные:\n"
            f"Сервис: {downtime.service}\n"
            f"Дата начала: {downtime.start_downtime}\n"
            f"Дата конца: {downtime.end_downtime}\n"
            f"Ссылка на проведение работ: {downtime.link_task}\n"
            f"Описание: {downtime.description}\n\n"
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {e}"
        )

    try:
        new_downtime = await create_post_request(downtime=downtime)
    except ErrorRequestDowntime as e:
        return await update.message.reply_text(
            str(e)
        )
    try:
        logger.info("Отправили успешный ответ о создании плановых работ")
        await update.message.reply_text(
            f"Плановые работы успешно созданы\n"
            f"id: {new_downtime}"
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )

    logger.info("Очистили context")
    context.user_data.clear()
    return ConversationHandler.END
