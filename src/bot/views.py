import asyncio
import json
import logging
from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View

from .bot import Bot

logger = logging.getLogger(__name__)


class BotUpdateView(View):
    """View for handling Telegram bot updates."""

    async def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse:
        """Handle the POST request from Telegram. Works as a webhook."""
        secret_key = request.META.get("HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN")
        if secret_key != settings.WEBHOOK_SECRET_KEY:
            logger.warning("Unauthorized access denied")
            return JsonResponse(
                status=HTTPStatus.UNAUTHORIZED, data={}, safe=False
            )

        bot = Bot.get_instance()
        asyncio.create_task(bot.process_update(data=json.loads(request.body)))
        return JsonResponse(
            status=HTTPStatus.OK, data={"ok": True}, safe=False
        )
