from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.api.requests_to_backend import authorized_user
from bot.constants import LOGIN, PASSWORD
from bot.decorators import check_type_chat
from bot.exceptions import ErrorRequestDowntime, ErrorSendMessage
from bot.logs_settings import logger
from bot.utils import User


@check_type_chat
async def login(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Получли запрос на авторизацию")
    context.user_data["user"] = User()
    try:
        logger.info("Отправили в чат запрос логина")
        await update.message.reply_text(
            "Введи Логин",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения: {str(e)}"
        )

    return LOGIN


async def password(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Получили логин")
    user: User = context.user_data.get("user")
    user.save_login(
        data=update.message.text.strip()
    )

    try:
        logger.info("Отправили в чат запрос пароля")
        await update.message.reply_text(
            "Введи пароль",
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения в чат: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {str(e)}"
        )
    return PASSWORD


async def check_personal_data(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Получили пароль")
    user: User = context.user_data.get("user")
    user.password = update.message.text

    try:
        logger.info("Отправили уведомление о проверке данных")
        await update.message.reply_text(text="Проверяю")
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения: {str(e)}"
        )

    try:
        await authorized_user(user=user)
    except ErrorRequestDowntime as e:
        await update.message.reply_text(
            f"Авторизация не пройдена: {str(e)}\n"
            f"Попробуй еще раз"
        )
        logger.info("Отправили повторный запрос на авторизацию")
        return await login(update=update, context=context)

    logger.info(
        f"Записали успешную авторизацию в context. "
        f"Пользователь: {user.username}"
    )
    context.user_data["authorized"] = True

    try:
        logger.info("Отправили успешный ответ в чат")
        await update.message.reply_text(text="Суккесс")
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке сообщения: {str(e)}")
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {str(e)}")

    return ConversationHandler.END
