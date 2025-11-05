from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.decorators import check_type_chat
from bot.exceptions import ErrorSendMessage


@check_type_chat
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    output = (
        f"Привет {update.message.from_user.username}.\n"
        f"Для продолжения необходимо авторизоваться\n"
    )
    reply_keyboard = [["/login"]]

    try:
        await update.message.reply_text(
            text=output, reply_markup=ReplyKeyboardMarkup(reply_keyboard)
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")


@check_type_chat
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
