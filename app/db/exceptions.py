"""
Модуль ошибок, связанных с БД.
"""
from http import HTTPStatus


class DBInstanceError(Exception):
    def __init__(self, received_instance, expected_instance) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Invalid instance. " \
                       f"Received '{str(type(received_instance))}' and expected '{str(type(expected_instance))}'."
        super().__init__(self.message)
