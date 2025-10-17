import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HEADERS = {"token": os.getenv("TOKEN_FOR_API")}
URL = "http://job-lk.hopto.org/api/downtime-data-bot/"
