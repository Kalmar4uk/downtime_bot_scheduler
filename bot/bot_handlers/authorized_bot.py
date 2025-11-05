from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import setup
from bot.api.requests_to_backend import authorized_user
from bot.bot_handlers import handlers
from bot.constants import LOGIN, PASSWORD
from bot.exceptions import ErrorRequestDowntime, ErrorSendMessage
from bot.utils import User


async def login(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["user"] = User()
    try:
        await update.message.reply_text(
            "Введи Логин",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    return LOGIN


async def password(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    user: User = context.user_data.get("user")
    user.save_login(
        data=update.message.text.strip()
    )

    try:
        await update.message.reply_text(
            "Введи пароль",
        )
    except Exception as e:
        raise ErrorSendMessage(
            f"Возникла ошибка при отправке сообщения в чат: {e}"
        )
    return PASSWORD


async def check_personal_data(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    user: User = context.user_data.get("user")
    user.password = update.message.text

    try:
        await update.message.reply_text(text="Проверяю")
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    try:
        await authorized_user(user=user)
    except ErrorRequestDowntime as e:
        await update.message.reply_text(
            f"Авторизация не пройдена: {str(e)}\n"
            f"Попробуй еще раз"
        )
        return await login(update=update, context=context)

    output_success = (
        "Можешь воспользоваться кнопками в меню"
    )

    try:
        await update.message.reply_text(text="Ништяк")
        await update.message.reply_text(
            text=output_success
        )
    except Exception as e:
        raise ErrorSendMessage(f"Возникла ошибка при отправке сообщения: {e}")

    context.user_data.clear()

    return await handlers.handlers_create_downtime(app=setup.app)
