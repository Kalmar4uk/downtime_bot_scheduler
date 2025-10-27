from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler,
                          filters)

from bot.bot_handlers.base import (cancel, description_for_create_donwtime,
                                   start)
from bot.bot_handlers.create_downtime import (calendar_for_added_store,
                                              check_date,
                                              desctiption_create_downtime,
                                              hour_create,
                                              link_create_downtime,
                                              minute_create,
                                              service_for_create_downtime)
from bot.constants import (CALENDAR, CHECK_DATE, DESCRIPTION, HOUR,
                           LINK, MINUTE, SERVICE)


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
            CALENDAR: [
                CallbackQueryHandler(calendar_for_added_store)
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
