from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import SERVICE
from bot.exceptions import ErrorSendMessage
from bot.utils import Downtime


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Описание команд"""
    output = (
        f"Привет {update.message.from_user.username}.\n"
        f"Отправь /add_downtime для добавления нового downtime\n"
        f"Либо воспользуйся кнопками в меню"
    )
    try:
        await update.message.reply_text(
            text=output
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")


async def description_for_create_donwtime(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["downtime"] = Downtime()
    try:
        await update.message.reply_text(
            "Для добавления Downtime необходимо поочередно написать:\n"
            "Сервис (прим. Siebel)\n"
            "Дата и время начала проведения работ\n"
            "Дата и время окончания проведения работ\n"
            "Ссылку на задачу\n"
            "Краткое описание работ\n"
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")
    return await create_downtime(update=update, context=context)


async def create_downtime(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    try:
        await update.message.reply_text(
            "Введи название сервиса или отправь /cancel для остановки"
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    return SERVICE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановка диалога"""

    try:
        await update.message.reply_text(
            "Запись остановлена"
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    context.user_data.clear()

    return ConversationHandler.END
