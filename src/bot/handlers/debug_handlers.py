import functools
import logging
from typing import Callable

from django.conf import settings

from bot.constants.states import States

logger = logging.getLogger("core")


def debug_logger(state: States, run_functions_debug_loger: str) -> Callable:
    """Log function for handlers."""

    def log(func: Callable) -> Callable:
        if not settings.DEBUG:
            return func

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if len(args) != 2:
                raise ValueError(f"Expected 2 arguments, but got {len(args)}")

            update, context = args
            user_id = "NONAME"
            message = "None"
            if update.message is not None:
                user_id = update.message.chat.id
                message = update.message.text

            query_data = "None"
            if update.callback_query is not None:
                query_data = update.callback_query.data
                user_id = update.callback_query.from_user.id
            try:
                logger.debug(
                    "User %s run %s, update data: %s, message: %s, state: %s",
                    user_id,
                    run_functions_debug_loger,
                    query_data,
                    message,
                    state,
                )
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    "Error %s after command: %s", e, run_functions_debug_loger
                )

        return wrapper

    return log
