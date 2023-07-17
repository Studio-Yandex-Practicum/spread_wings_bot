import os
from ast import literal_eval
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env", raise_error_if_not_found=True))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = literal_eval(os.environ.get("DEBUG", "True"))

# TODO: hide to env and parse
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bot.apps.BotConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", default="postgres"),
        "USER": os.environ.get("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", default="localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", default="5432"),
    },
}
DB_URL = os.environ.get("DB_URL")  # legacy, probably

REDIS = {
    "host": os.environ.get("REDIS_HOST"),
    "port": os.environ.get("REDIS_PORT"),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MAILING = {
    "host": os.environ.get("EMAIL_HOST"),
    "port": os.environ.get("EMAIL_PORT"),
    "account": os.environ.get("EMAIL_ACCOUNT"),
    "password": os.environ.get("EMAIL_PASSWORD"),
    "default_address": os.environ.get("DEFAULT_EMAIL_ADDRESS"),
}

# Telegram bot settings
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
USE_REDIS_PERSISTENCE = literal_eval(os.environ.get("REDIS", "False"))
WEBHOOK_ENABLED = literal_eval(os.environ.get("WEBHOOK_ENABLED", "False"))
WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL", "http://127.0.0.1:8000/bot/webhook/"
)
WEBHOOK_SECRET_KEY = os.environ.get("WEBHOOK_SECRET_KEY", "not-so-secret-key")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s - [%(levelname)s] - %(message)s",
            "datefmt": "%d.%m.%Y %H:%M:%S",
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default_formatter",
            "filename": BASE_DIR / "logs" / "bot.log",
            "maxBytes": 10**6,
            "backupCount": 5,
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["stream_handler", "file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}
