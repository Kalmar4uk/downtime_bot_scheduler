from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters, ContextTypes)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from bot.bot_handlers.base import start, description_for_create_donwtime, cancel
from bot.bot_handlers.create_downtime import service_for_create_downtime, date_start_create_downtime, date_end_create_downtime, link_create_downtime, desctiption_create_downtime
from bot.constants import SERVICE, DATE_START, DATE_END, LINK, DESCRIPTION


async def start_handler(app: Application):
    app.add_handler(CommandHandler("start", start))


async def handlers_create_downtime(app: Application) -> None:

    create_downtime = ConversationHandler(
        entry_points=[
            CommandHandler("add_downtime", description_for_create_donwtime)
        ],
        states={
            SERVICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    service_for_create_downtime
                )
            ],
            DATE_START: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    date_start_create_downtime
                )
            ],
            DATE_END: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    date_end_create_downtime
                )
            ],
            LINK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    link_create_downtime
                )
            ],
            DESCRIPTION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    desctiption_create_downtime
                )
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(create_downtime)
