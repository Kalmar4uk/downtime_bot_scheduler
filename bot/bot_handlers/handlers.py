from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)

from bot import setup
from bot.bot_handlers.authorized_bot import (check_personal_data, login,
                                             password)
from bot.bot_handlers.base import cancel, start
from bot.bot_handlers.create_downtime import (calendar_create,
                                              calendar_for_create_downtime,
                                              check_date,
                                              desctiption_create_downtime,
                                              hour_create,
                                              link_create_downtime,
                                              minute_create,
                                              service_for_create_downtime)
from bot.constants import (CALENDAR, CHECK_DATE, DESCRIPTION, HOUR, LINK,
                           LOGIN, MINUTE, MY_COMMANDS, PASSWORD, SERVICE)


async def start_handler(app: Application):
    app.add_handler(CommandHandler("start", start))


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error

    if update:
        await update.effective_chat.send_message(
            f"Возникла ошибка в работе бота: {error}"
        )


async def handlers_create_downtime(app: Application) -> None:

    create_downtime = ConversationHandler(
        entry_points=[
            CommandHandler("add_downtime", service_for_create_downtime)
        ],
        states={
            SERVICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    calendar_for_create_downtime
                )
            ],
            CALENDAR: [
                CallbackQueryHandler(calendar_create)
            ],
            HOUR: [
                CallbackQueryHandler(hour_create)
            ],
            MINUTE: [
                CallbackQueryHandler(minute_create)
            ],
            CHECK_DATE: [
                CallbackQueryHandler(check_date)
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
    await setup.app.bot.set_my_commands(MY_COMMANDS)


async def handlers_authorized(app: Application) -> None:

    authorized = ConversationHandler(
        entry_points=[
            CommandHandler("login", login)
        ],
        states={
            LOGIN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    password
                )
            ],
            PASSWORD: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    check_personal_data
                )
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(authorized)
