import json
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import DetailedTelegramCalendar

from bot.constants import DATE_FORMAT, TIME_FORMAT


class Downtime:

    def __init__(
            self,
            service: str | None = None,
            link: str | None = None,
            description: str | None = None,
            start: datetime | None = None,
            end: datetime | None = None,
            first_name: str | None = None,
            last_name: str | None = None
    ):
        self.service = service
        self.link = link
        self.description = description
        self.start = start
        self.end = end
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def preparation(cls, data: dict):
        employee: dict = data.get("gsma_employee")
        try:
            start: datetime = datetime.fromisoformat(
                data.get("start_downtime")
            )
            end: datetime = datetime.fromisoformat(
                data.get("end_downtime")
            )
        except Exception:
            start = None
            end = None
        return cls(
            service=data.get("service"),
            link=data.get("link_task"),
            description=data.get("description"),
            start=start,
            end=end,
            first_name=employee.get("first_name"),
            last_name=employee.get("last_name"),
        )

    def save_service_and_description(
            self,
            data: str,
            is_service: bool = False
    ) -> None:
        if not isinstance(data, str):
            raise Exception
        data = data.capitalize()
        if is_service:
            self.service = data
        else:
            self.description = data

    def save_start_and_end_date(
            self,
            data: str,
            start: bool = False
    ) -> None:
        try:
            date_downtime = datetime.strptime(data, f"{DATE_FORMAT} {TIME_FORMAT}")
        except ValueError as e:
            raise ValueError(str(e))
        if start:
            self.start = date_downtime
        else:
            self.end = date_downtime


async def generate_calendar() -> InlineKeyboardMarkup:
    """Генерация календаря"""
    calendar_json, _ = DetailedTelegramCalendar(locale="ru").build()
    calendar_data = json.loads(calendar_json)

    return InlineKeyboardMarkup(calendar_data["inline_keyboard"])


async def generate_hour() -> InlineKeyboardMarkup:
    keyboard = []
    hours = [f"{h}" for h in range(0, 24)]
    for i in range(0, len(hours), 6):
        row = [
            InlineKeyboardButton(
                f"{h}", callback_data=f"{h}"
            ) for h in hours[i:i+6]
        ]
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


async def generate_minute() -> InlineKeyboardMarkup:
    keyboard = []
    minutes = [f"{m}" for m in range(0, 60)]
    for i in range(0, len(minutes), 6):
        row = [
            InlineKeyboardButton(
                m, callback_data=f"{m}"
            ) for m in minutes[i:i+6]
        ]
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)