import requests

from telegram.ext import ApplicationBuilder
from bot.constants import URL, HEADERS, CHAT_ID
from bot.utils import PreparationForMessage


async def get_downtime(app: ApplicationBuilder) -> None:
    downtime: dict = requests.get(URL, headers=HEADERS).json()[0]  # Api отдает массив объектов, надо будет переписать на случай, если объектов > 1
    if downtime:
        message = PreparationForMessage.preparation(data=downtime)
        await sent_message(data=message, app=app)


async def sent_message(
        data: PreparationForMessage,
        app: ApplicationBuilder
) -> None:
    text: str = (
        f"{data.start.date()}\nС {data.start.time()} По {data.end.time()}\n"
        f"Будет произведено: {data.description}\nCервиса {data.service}\n"
        f"Ответственный со стороны ГСМАиЦП:\n"
        f"{data.last_name} {data.first_name}"
    )
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"Возникла ошибка {e}")
