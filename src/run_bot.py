from telegram.ext import ApplicationBuilder

from bot.handlers.assistance import assistance_handler  # , help_handler
from bot.core.config import settings


def main():
    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handler(assistance_handler)
    # app.add_handler(help_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
