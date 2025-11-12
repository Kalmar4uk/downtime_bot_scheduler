import os

from dotenv import load_dotenv
from telegram import BotCommand

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MY_CHAT = os.getenv("MY_CHAT")
HEADERS = {"token": os.getenv("TOKEN_FOR_API")}
URL = "https://job-lk.hopto.org/api/downtime/?start_from={}&start_to={}"
URL_LOGIN = "https://job-lk.hopto.org/api/v2/token/login/"

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
LOGIN, PASSWORD = range(2)
PATTERN_LINK = r"^https://tracker\.yandex\.ru/DOWNTIME-\d{1,}"
MY_COMMANDS = (
    BotCommand("start", "Начало работы"),
    BotCommand("login", "Авторизоваться"),
    BotCommand("add_downtime", "Добавить плановые работы"),
    BotCommand("cancel", "Остановить запись плановых работ")
)
