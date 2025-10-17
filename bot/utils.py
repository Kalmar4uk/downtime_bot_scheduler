from datetime import datetime


class PreparationForMessage:

    def __init__(
            self,
            service: str | None,
            link: str | None,
            description: str | None,
            start: datetime | None,
            end: datetime | None,
            first_name: str | None,
            last_name: str | None
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
