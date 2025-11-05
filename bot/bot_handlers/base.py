from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import setup
from bot.bot_handlers import handlers
from bot.exceptions import ErrorSendMessage


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type != "private":
        return await update.message.reply_text(
            "Бот используется для добавления плановых работ.\n\n"
            "Плановые работы возможно добавить только из личного чата.\n"
            "Необходимо написать боту в личные сообщения"
        )
    output = (
        f"Привет {update.message.from_user.username}.\n"
        f"Для продолжения необходимо авторизоваться\n"
        f"Нажми на кнопку или отправь /login"
    )
    reply_keyboard = [["/login"]]
    try:
        await update.message.reply_text(
            text=output, reply_markup=ReplyKeyboardMarkup(reply_keyboard)
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    await handlers.handlers_authorized(app=setup.app)


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
