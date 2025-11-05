from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


def require_auth(func):
    """Декоратор для проверки авторизации"""
    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs
    ):
        if not context.user_data.get("authorized"):
            await update.message.reply_text(
                "Для использования этой команды необходимо авторизоваться.\n"
                "Используйте /login для авторизации"
            )
            return ConversationHandler.END
        return await func(update, context, *args, **kwargs)
    return wrapper


def check_type_chat(func):
    """Декоратор проверки типа чата приват/группа"""
    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs
    ):
        if update.message.chat.type != "private":
            await update.message.reply_text(
                "Бот используется для добавления плановых работ.\n\n"
                "Плановые работы возможно добавить только из личного чата.\n"
                "Необходимо написать боту в личные сообщения"
            )
            return ConversationHandler.END
        return await func(update, context, *args, **kwargs)
    return wrapper
