from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.decorators import check_type_chat
from bot.exceptions import ErrorSendMessage
from bot.logs_settings import logger


@check_type_chat
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Запущена функция start")
    output = (
        f"Привет {update.message.from_user.username}.\n"
        f"Для продолжения необходимо авторизоваться\n"
    )
    reply_keyboard = [["/login"]]

    try:
        logger.info("Отправили приветствие в чат")
        await update.message.reply_text(
            text=output, reply_markup=ReplyKeyboardMarkup(reply_keyboard)
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения: {str(e)}"
        )


@check_type_chat
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановка диалога"""
    logger.info("Запущена остановка записи плановых работ")

    try:
        logger.info("Отправили уведомление об остановке")
        await update.message.reply_text(
            "Запись остановлена"
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    logger.info("Очистили context")
    context.user_data.clear()

    return ConversationHandler.END
