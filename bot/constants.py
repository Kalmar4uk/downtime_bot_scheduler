import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HEADERS = {"token": os.getenv("TOKEN_FOR_API")}
URL = "http://job-lk.hopto.org/api/downtime-data-bot/"

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

SERVICE, CALENDAR, HOUR, MINUTE, CHECK_DATE, DATE_END, LINK, DESCRIPTION = range(8)
PATTERN_LINK = r"^https://tracker\.yandex\.ru/DOWNTIME-\d{1,}"
