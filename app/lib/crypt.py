"""
Модуль хэширования и верификации паролей.
"""
import random

from passlib.hash import pbkdf2_sha256
from pydantic import SecretBytes, SecretStr
from litestar.utils.sync import AsyncCallable

from app import db


def generate_password(password_max_length=16) -> str:
    """
    Функция генерации паролей.

    :param password_max_length: максимальная длина пароля.

    :return: сгенерированный пароль.
    """
    password_required_chars = ['abcdefghijklnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '1234567890']
    password = ''

    password_length = random.randint(db.consts.MIN_LEN_USER_PASSWORD, password_max_length)
    for i in range(password_length - len(password_required_chars)):
        password += random.choice(''.join(password_required_chars))

    required_chars = [random.choice(chars) for chars in password_required_chars]
    for char in required_chars:
        insert_index = random.randint(0, len(password))
        password = password[:insert_index] + char + password[insert_index:]

    return password


async def get_password_hash(password: SecretBytes | SecretStr | str | bytes) -> str:
    """Функция возвращает хэш пароля.

    :param password: Пароль.
    :return: Хэшированный пароль.
    """
    if isinstance(password, SecretBytes | SecretStr):
        password = password.get_secret_value()
    return await AsyncCallable(pbkdf2_sha256.hash)(secret=password)


async def verify_password(plain_password: SecretBytes | SecretStr | str | bytes, hashed_password: str) -> bool:
    """Функция верификации пароля.

    :param plain_password: Пароль.
    :param hashed_password: Хэшированный пароль.
    :return: True если хэши паролей совпадают.
    """
    if isinstance(plain_password, SecretBytes | SecretStr):
        plain_password = plain_password.get_secret_value()

    valid_identify = await AsyncCallable(pbkdf2_sha256.identify)(
        hash=hashed_password,
    )
    if not valid_identify: return False

    valid = await AsyncCallable(pbkdf2_sha256.verify)(
        secret=plain_password,
        hash=hashed_password,
    )
    return bool(valid)
