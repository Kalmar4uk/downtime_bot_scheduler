import re
from telegram import (InlineKeyboardMarkup, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

from bot.constants import DATE_START, DATE_END, LINK, DESCRIPTION, PATTERN_LINK
from bot.utils import Downtime


async def service_for_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Получение название сервиса"""
    downtime: Downtime = context.user_data.get("downtime")
    downtime.save_service_and_description(
        data=update.message.text.strip(),
        is_service=True
        )
    await update.message.reply_text(
        "Введи дату старта в формате ДД.ММ.ГГГГ"
        "или отправь /cancel для остановки"
    )
    return DATE_START


async def date_start_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    downtime: Downtime = context.user_data.get("downtime")
    try:
        downtime.save_start_and_end_date(data=update.message.text, start=True)
    except ValueError as e:
        await update.message.reply_text(
            f"Возникла ошибка проверь дату: {e}"
        )
        return DATE_START
    await update.message.reply_text(
        "Введи дату окончания в формате ДД.ММ,ГГГГ "
        "или отправь /cancel для остановки"
    )
    return DATE_END


async def date_end_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    downtime: Downtime = context.user_data.get("downtime")
    try:
        downtime.save_start_and_end_date(data=update.message.text, start=True)
    except ValueError as e:
        await update.message.reply_text(
            f"Возникла ошибка проверь дату: {e}"
        )
        return DATE_END
    await update.message.reply_text(
        "Введи ссылку на проведение работ или "
        "отправь /cancel для остановки"
    )
    return LINK


async def link_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    link = update.message.text.strip()
    if not re.match(PATTERN_LINK, link):
        await update.message.reply_text(
            "Это не похоже на корректную ссылку на даунтайм.\n"
            "Пожалуйста, нужна ссылка в формате:\n"
            "https://tracker.yandex.ru/DOWNTIME-XXXX\n\n"
        )
        return LINK
    downtime: Downtime = context.user_data.get("downtime")
    downtime.link = link
    await update.message.reply_text("Введи краткое описание работ")
    return DESCRIPTION


async def desctiption_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    downtime: Downtime = context.user_data.get("downtime")
    downtime.save_service_and_description(data=update.message.text.strip())
    await update.message.reply_text("Записал новый downtime")
    return ConversationHandler.END
