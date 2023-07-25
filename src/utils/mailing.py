import re
import smtplib

from django.conf import settings

from bot.exceptions import InvalidRecipientEmailAddress
from bot.models_pydantic.users_questions import UserQuestion


class BotMailer:
    """Класс для отправки сообщений на почту."""

    SMTP_SERVER = settings.MAILING["host"]
    SERVER_PORT = settings.MAILING["port"]
    SENDER_ACCOUNT = settings.MAILING["account"]
    SENDER_PASSWORD = settings.MAILING["password"]
    DEFAULT_SUBJECT = "Вопрос из телеграм бота"
    DEFAULT_ADDRESS = settings.MAILING["default_address"]
    EMAIL_TEMPLATE = "From: {}\nTo: {}\nSubject: {}\n\n{}"
    TEXT_TEMPLATE = (
        "Пользователь {} (контакт для связи: {})\n"
        "Тема вопроса: {}\nВопрос: {}"
    )
    REG = r"[^@]+@[^@]+\.[^@]+"

    @classmethod
    def _validate_address(cls, address):
        if not re.fullmatch(cls.REG, address):
            raise InvalidRecipientEmailAddress("Некорректный адресат")

    @classmethod
    async def send_message(
        cls,
        mail_form: UserQuestion,
        address=DEFAULT_ADDRESS,
        subject=DEFAULT_SUBJECT,
    ):
        """
        Метод отправки сообщения.

        Примет целевой адрес, тему и текст,
        провалидирует адрес, отправит сообщение с помощью сервера, указанного
        в настройках проект, от имени аккаунта, указанного в настройках проекта.
        """
        cls._validate_address(address)
        smtp_object = smtplib.SMTP_SSL(cls.SMTP_SERVER, cls.SERVER_PORT)
        smtp_object.login(cls.SENDER_ACCOUNT, cls.SENDER_PASSWORD)
        text = cls.TEXT_TEMPLATE.format(
            mail_form.name,
            mail_form.contact,
            mail_form.question_type,
            mail_form.question,
        )
        msg = cls.EMAIL_TEMPLATE.format(
            cls.SENDER_ACCOUNT, address, subject, text
        ).encode("utf-8")
        with smtp_object as s:
            s.sendmail(cls.SENDER_ACCOUNT, cls.DEFAULT_ADDRESS, msg)
