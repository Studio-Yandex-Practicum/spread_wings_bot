from pathlib import Path

import environ
from dotenv import find_dotenv

env = environ.Env()
if DEBUG := env.bool("DEBUG", default=True):
    environ.Env.read_env(find_dotenv(".env", raise_error_if_not_found=True))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bot.apps.BotConfig",
    "users.apps.UsersConfig",
    "core.apps.CoreConfig",
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
    "default": env.db_url(
        "DATABASE_URL", engine="django.db.backends.postgresql"
    ),
}

REDIS = {
    "host": env.str("REDIS_HOST"),
    "port": env.str("REDIS_PORT"),
}

AUTH_USER_MODEL = "users.User"

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
    "host": env.str("EMAIL_HOST"),
    "port": env.str("EMAIL_PORT"),
    "account": env.str("EMAIL_ACCOUNT"),
    "password": env.str("EMAIL_PASSWORD"),
    "default_address": env.str("DEFAULT_EMAIL_ADDRESS"),
}

# Telegram bot settings
TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
USE_REDIS_PERSISTENCE = env.bool("REDIS", default=False)
WEBHOOK_ENABLED = env.bool("WEBHOOK_ENABLED", default=False)
WEBHOOK_URL = env.str("WEBHOOK_URL", default=None)
WEBHOOK_SECRET_KEY = env.str("WEBHOOK_SECRET_KEY", default=None)

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
