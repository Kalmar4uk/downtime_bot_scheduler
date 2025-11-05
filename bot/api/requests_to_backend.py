import requests

from bot.constants import HEADERS, URL, URL_LOGIN
from bot.exceptions import ErrorRequest, ErrorRequestDowntime
from bot.logs_settings import logger
from bot.utils import Downtime, User


async def create_post_request(downtime: Downtime):
    data = downtime.__dict__

    del data["first_name"]
    del data["last_name"]

    try:
        logger.info("Отправили запрос на создание плановых работ")
        response = requests.post(URL, data=data, headers=HEADERS)
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке запроса: {str(e)}")
        raise ErrorRequest(
            f"Возникла ошибка при отправке запроса: {e}"
        )

    if response.status_code == 201:
        return response.json().get("id")

    logger.error(
            f"Получили не успешный ответ: "
            f"{response.status_code} {response.json()}"
        )
    raise ErrorRequestDowntime(
        f"Статус код: {response.status_code} "
        f"Ответ сервера: {response.json()}"
    )


async def authorized_user(user: User):
    data = user.__dict__

    try:
        logger.info("Отправили запрос проверки логина и пароля")
        response = requests.post(
            URL_LOGIN, data=data, params={"bot": True}
        )
    except Exception as e:
        logger.error(f"Возникла ошибка при отправке запроса: {str(e)}")
        raise ErrorRequest(
            f"Возникла ошибка при отправке запроса: {str(e)}"
        )
    if response.status_code != 200:
        logger.error(
            f"Получили не успешный ответ: "
            f"{response.status_code} {response.json()}"
        )
        raise ErrorRequestDowntime(
            f"Статус код: {response.status_code}\n"
            f"Ответ сервера: {response.json()}"
        )
