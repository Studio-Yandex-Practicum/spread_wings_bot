from telegram.ext import Application, CallbackQueryHandler, ConversationHandler

from bot.constants.states import ASSISTANCE, DONATION
from bot.core.config import settings
from bot.handlers.assistance import make_donation, receive_assistance
from bot.handlers.main_handlers import help_handler, start_handler


def main():
    app = Application.builder().token(settings.telegram_token).build()
    conv_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            ASSISTANCE: [
                CallbackQueryHandler(
                    receive_assistance,
                    pattern=f'^{ASSISTANCE}$'
                    ),
                CallbackQueryHandler(make_donation, pattern=f'^{DONATION}$')
            ]
        },
        fallbacks=[
            start_handler,
        ],
    )
    app.add_handlers([conv_handler, help_handler])
    app.run_polling()


if __name__ == '__main__':
    main()
