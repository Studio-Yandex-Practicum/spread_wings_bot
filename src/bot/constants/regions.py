import asyncio
import threading
from enum import StrEnum

from bot.db.db import start_session
from bot.parsing_data import get_regions

loop = asyncio.new_event_loop()
thread = threading.Thread(target=asyncio.set_event_loop, args=(loop,))
thread.start()
session = asyncio.run(start_session())
regions = asyncio.run(get_regions(session))
Regions = StrEnum(list(regions.keys())[0], list(regions.values())[0])
loop.close()
