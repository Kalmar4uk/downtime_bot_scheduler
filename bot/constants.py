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
    "Необходимо оформить рассылку сегодня в {}:\n"
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
