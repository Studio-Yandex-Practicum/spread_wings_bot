from pathlib import Path

import environ
from dotenv import find_dotenv

env = environ.Env()

environ.Env.read_env(find_dotenv(".env"))

DEBUG = env.bool("DEBUG", default=True)

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
    "bot_settings.apps.BotSettingsConfig",
    "bot.apps.BotConfig",
    "users.apps.UsersConfig",
    "core.apps.CoreConfig",
    "ckeditor",
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
        "DIRS": [BASE_DIR / "templates"],
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

ASGI_APPLICATION = "config.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
    },
}

REDIS = {
    "host": env.str("REDIS_HOST"),
    "port": env.str("REDIS_PORT"),
}

AUTH_USER_MODEL = "users.user"

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

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATIC_ROOT.mkdir(exist_ok=True)
STATICFILES_DIRS = [
    ("ckeditor/ckeditor/plugins", "src/ckeditor_add-on/plugins/"),
    ("ckeditor/ckeditor/skins", "src/ckeditor_add-on/skins/"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_TEMPLATE_NAME = "email.html"
EMAIL_HOST = env.str("EMAIL_HOST")

try:
    EMAIL_PORT = env.int("EMAIL_PORT")
except ValueError:
    EMAIL_PORT = 465

EMAIL_HOST_USER = env.str("EMAIL_ACCOUNT")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD")
EMAIL_TIMEOUT = 5  # seconds
EMAIL_USE_SSL = True
DEFAULT_RECEIVER = env.str("DEFAULT_EMAIL_ADDRESS")

# Telegram bot settings
TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
USE_REDIS_PERSISTENCE = env.bool("REDIS", default=False)
KEYBOARDS_CACHE_TTL = env.float("KEYBOARDS_CACHE_TTL", default=600)
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
            "class": "core.custom_handler.CustomRotatingFileHandler",
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
        },
        "core": {
            "handlers": ["stream_handler", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

CKEDITOR_CONFIGS = {
    "default": {
        "allowedContent": {
            "strong em u s a": {
                "attributes": True,
                "styles": False,
                "classes": False,
            }
        },
        "autoParagraph": False,
        "basicEntities": False,
        "enterMode": 2,
        "extraPlugins": ["autocomplete", "emoji", "textmatch", "textwatcher"],
        "forcePasteAsPlainText": True,
        "height": 300,
        "ignoreEmptyParagraph": True,
        "language": "ru",
        "removePlugins": "stylesheetparser",
        "resize_enabled": False,
        "skin": "n1theme",
        "toolbar": "Custom",
        "toolbarCanCollapse": False,
        "toolbar_Custom": [
            {
                "name": "upper_buttons",
                "items": [
                    "NewPage",
                    "Preview",
                    "-",
                    "Undo",
                    "Redo",
                    "-",
                    "Copy",
                    "Paste",
                    "Cut",
                    "-",
                    "Find",
                    "Replace",
                    "-",
                    "Maximize",
                    "-",
                    "About",
                ],
            },
            "/",
            {
                "name": "lower_buttons",
                "items": [
                    "SelectAll",
                    "-",
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "RemoveFormat",
                    "-",
                    "Link",
                    "Unlink",
                    "-",
                    "SpecialChar",
                    "EmojiPanel",
                ],
            },
        ],
        "width": "full",
    },
}
