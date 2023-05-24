from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.handlers.main_handlers import start_handler, help_handler
from bot.core.config import settings

START_ROUTES, END_ROUTES = range(2)


def main():
    app = Application.builder().token(settings.telegram_token).build()
    #conv_handler = ConversationHandler(
    #    entry_points=[CommandHandler("start", start_handler)],
    #    states={
    #        START_ROUTES: [
    #            CommandHandler("help", help_handler)
    #        ],
    #    },
    #    fallbacks=[
    #        CommandHandler("start", start_handler),
    #        CommandHandler("help", help_handler)
    #    ]
    #)
    app.add_handlers([start_handler, help_handler])
    app.run_polling()


if __name__ == '__main__':
    main()
