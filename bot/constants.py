import os

from dotenv import load_dotenv
from telegram import BotCommand

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HEADERS = {"token": os.getenv("TOKEN_FOR_API")}
URL = "https://job-lk.hopto.org/api/downtime/"

DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"

NEWSLETTER = (
    "Необходимо оформить рассылку сегодня в <b>{}</b>:\n"
    "1. По почте;\n"
    "2. В чатах месседжер:\n"
    " - Срочные оповещения;\n"
    " - Срочные_ИТ;\n"
    " - Срочные_ОКПЦС;\n"
    " - Срочные_Омни;\n"
    " - Срочные Siebel;\n"
    " - Срочные_Hybris;\n"
    " - Срочные_Даркстор"
)

SERVICE, CALENDAR, HOUR, MINUTE, CHECK_DATE, LINK, DESCRIPTION = range(7)
PATTERN_LINK = r"^https://tracker\.yandex\.ru/DOWNTIME-\d{1,}"
MY_COMMANDS = (
    BotCommand("start", "Начало"),
    BotCommand("add_downtime", "Добавить плановые работы"),
    BotCommand("cancel", "Остановить запись плановых работ")
)
