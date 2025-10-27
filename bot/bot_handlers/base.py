from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import SERVICE
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
        print(f"Возникла ошибка при отправке сообщения: {e}")


async def description_for_create_donwtime(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["downtime"] = Downtime()
    await update.message.reply_text(
        "Для добавления Downtime необходимо поочередно написать:\n"
        "Сервис (прим. Siebel)\n"
        "Дата и время начала проведения работ\n"
        "Дата и время окончания проведения работ\n"
        "Ссылку на задачу\n"
        "Краткое описание работ\n"
    )
    return await create_downtime(update=update, context=context)


async def create_downtime(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text(
        "Введи название сервиса или отправь /cancel для остановки"
    )
    return SERVICE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановка диалога"""
    await update.message.reply_text(
        "Запись остановлена"
    )
    context.user_data.clear()
    return ConversationHandler.END
