import json
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional, Tuple

from redis.asyncio import Redis
from telegram.ext import BasePersistence

from bot.core.config import settings

redis_instance = Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


class RedisPersistence(BasePersistence):
    """Using Redis to make the bot persistent."""

    def __init__(self, redis, on_flush: bool = False):
        """Init class."""
        super().__init__(update_interval=1)

        self.redis = redis
        self.on_flush = on_flush
        self.user_data: Optional[Dict[int, Dict]] = None
        self.chat_data: Optional[Dict[int, Dict]] = None
        self.bot_data: Optional[Dict] = None
        self.conversations: Optional[Dict[str, Dict[Tuple, Any]]] = None

    async def load_redis(self) -> None:
        """Load data from redis."""
        try:
            json_data = await self.redis.get("TelegramBotPersistence")
            if json_data:
                data = json.loads(json_data)
                self.user_data = defaultdict(dict, data["user_data"])
                self.chat_data = defaultdict(dict, data["chat_data"])
                self.bot_data = defaultdict(dict, data["bot_data"])
                self.conversations = defaultdict(dict, data["conversations"])
            else:
                self.conversations = dict()
                self.user_data = defaultdict(dict)
                self.chat_data = defaultdict(dict)
                self.bot_data = {}
        except Exception as e:
            print(e)

    async def dump_redis(self) -> None:
        """Copy dict to Redis."""
        data = {
            "conversations": self.conversations,
            "user_data": self.user_data,
            "chat_data": self.chat_data,
            "bot_data": self.bot_data,
        }
        json_images = json.dumps(data)
        await self.redis.set("TelegramBotPersistence", json_images)

    async def get_user_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        """Return the user_data."""
        if self.user_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.user_data)

    async def get_chat_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        """Return the chat_data."""
        if self.chat_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.chat_data)

    async def get_bot_data(self) -> Dict[Any, Any]:
        """Return the bot_data."""
        if self.bot_data:
            pass
        else:
            await self.load_redis()
        return deepcopy(self.bot_data)

    async def get_conversations(self, name: str):
        """Return the conversations."""
        if self.conversations:
            pass
        else:
            await self.load_redis()
        conversations = {}
        for key, value in self.conversations.get(name, {}).items():
            conversations[tuple(map(int, key.split()))] = value
        return conversations

    async def update_conversation(
        self, name: str, key: Tuple[int, ...], new_state: Optional[object]
    ) -> None:
        """Will update the conversations for the given handler.

        Depends on :attr:`on_flush` - save on Redis.
        """
        key = " ".join(map(str, key))
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            await self.dump_redis()

    async def update_user_data(self, user_id: int, data: Dict) -> None:
        """Will update the user_data.

        Depends on :attr:`on_flush` - save on Redis.
        """
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            await self.dump_redis()

    async def update_chat_data(self, chat_id: int, data: Dict) -> None:
        """Will update the chat_data.

        Depends on :attr:`on_flush` - save on Redis.
        """
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            await self.dump_redis()

    async def update_bot_data(self, data: Dict) -> None:
        """Will update the bot_data.

        Depends on :attr:`on_flush` - save on Redis.
        """
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            await self.dump_redis()

    async def flush(self) -> None:
        """Will save all data in memory to Redis."""
        await self.dump_redis()

    async def drop_user_data(self, user_id: int) -> None:
        """Not used."""
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        """Not used."""
        pass

    async def get_callback_data(self) -> Optional[Any]:
        """Not used."""
        pass

    async def refresh_bot_data(self, bot_data) -> None:
        """Not used."""
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: Any) -> None:
        """Not used."""
        pass

    async def refresh_user_data(self, user_id: int, user_data: Any) -> None:
        """Not used."""
        pass

    async def update_callback_data(self, data: Any) -> None:
        """Not used."""
        pass


persistence = RedisPersistence(redis_instance)
