import re
import smtplib

from bot.core.config import settings


class InvalidEmailAddress(Exception):
    """Кастомный эксепшн для поднятия при невалидном адресате."""

    pass


class BotMailer:
    """Класс для отправки сообщений на почту."""

    SMTP_SERVER = settings.email_host
    SERVER_PORT = settings.email_port
    SENDER_ACCOUNT = settings.email_account
    SENDER_PASSWORD = settings.email_password
    MSG_TEMPLATE = "From: {}\nTo: {}\nSubject: {}\n\n{}"
    REG = r"[^@]+@[^@]+\.[^@]+"

    @classmethod
    def _validate_address(cls, address):
        if not re.fullmatch(cls.REG, address):
            raise InvalidEmailAddress("Некорректный формат адреса")

    @classmethod
    def send_message(cls, address, subject, message):
        """
        Метод отправки сообщения.

        Примет целевой адрес, тему и текст,
        провалидирует адрес, отправит сообщение с помощью сервера, указанного
        в настройках проект, от имени аккаунта, указанного в настройках проекта.
        """
        cls._validate_address(address)
        smtp_object = smtplib.SMTP_SSL(cls.SMTP_SERVER, cls.SERVER_PORT)
        smtp_object.login(cls.SENDER_ACCOUNT, cls.SENDER_PASSWORD)
        msg = cls.MSG_TEMPLATE.format(
            cls.SENDER_ACCOUNT, address, subject, message
        ).encode("utf-8")
        with smtp_object as s:
            s.sendmail(cls.SENDER_ACCOUNT, address, msg)
