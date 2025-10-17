import requests
from telegram.ext import ApplicationBuilder

from bot.constants import CHAT_ID, DATE_FORMAT, HEADERS, TIME_FORMAT, URL
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
        f"<b>{data.start.date().strftime(DATE_FORMAT)}</b>\n"
        f"С <b>{data.start.time().strftime(TIME_FORMAT)}</b> "
        f"По <b>{data.end.time().strftime(TIME_FORMAT)}</b>\n"
        f"Cервис: <b>{data.service}</b>\n"
        f"Будет произведено: <b>{data.description}</b>\n"
        f"Ответственный со стороны ГСМАиЦП:\n"
        f"<b>{data.last_name} {data.first_name}</b>"
    )
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")
    except Exception as e:
        print(f"Возникла ошибка {e}")
