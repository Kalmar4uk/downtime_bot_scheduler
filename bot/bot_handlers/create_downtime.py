from telegram import (InlineKeyboardMarkup, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

from bot.constants import DATE_START, DATE_END, LINK, DESCRIPTION


async def service_for_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Получение название сервиса"""
    await update.message.reply_text("Введи дату старта в формате ДД.ММ.ГГГГ")
    return DATE_START


async def date_start_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("Введи дату окончания в формате ДД.ММ,ГГГГ")
    return DATE_END


async def date_end_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("Введи ссылку на проведение работ")
    return LINK


async def link_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("Введи краткое описание работ")
    return DESCRIPTION


async def desctiption_create_downtime(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("Записал новый downtime")
    return ConversationHandler.END
