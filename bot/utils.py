import json
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import DetailedTelegramCalendar

from bot.constants import DATE_FORMAT, TIME_FORMAT


class Downtime:

    def __init__(
            self,
            service: str | None = None,
            link_task: str | None = None,
            description: str | None = None,
            start_downtime: datetime | None = None,
            end_downtime: datetime | None = None,
            first_name: str | None = None,
            last_name: str | None = None
    ):
        self.service = service
        self.link_task = link_task
        self.description = description
        self.start_downtime = start_downtime
        self.end_downtime = end_downtime
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def preparation(cls, data: dict):
        employee: dict = data.get("gsma_employee")
        try:
            start_downtime: datetime = datetime.fromisoformat(
                data.get("start_downtime")
            )
            end_downtime: datetime = datetime.fromisoformat(
                data.get("end_downtime")
            )
        except Exception:
            start_downtime = None
            end_downtime = None
        return cls(
            service=data.get("service"),
            link_task=data.get("link_task"),
            description=data.get("description"),
            start_downtime=start_downtime,
            end_downtime=end_downtime,
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