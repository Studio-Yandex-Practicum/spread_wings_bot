import asyncio
from enum import StrEnum

from bot.parsing_data import get_regions

regions = asyncio.run(get_regions())
Regions = StrEnum(list(regions.keys())[0], list(regions.values())[0])
