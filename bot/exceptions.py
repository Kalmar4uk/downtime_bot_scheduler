class ErrorStartSchedule(Exception):
    """Исключение ошибки старта планировщика"""
    pass


class ErrorSendMessage(Exception):
    """Исключение ошибки отправления сообщения"""
    pass


class ErrorRequestDowntime(Exception):
    """Исключение при не удачной записи плановых работ на бекенд"""
    pass


class ErrorTransformDatetime(Exception):
    """Исключение при преобразовании строки в datetime"""
    pass


class ErrorRequest(Exception):
    """Исключение при отправке запроса"""
