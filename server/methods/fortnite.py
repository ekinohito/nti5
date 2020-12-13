import asyncio
import random
import time
from typing import Dict, Union

from aiohttp import ClientSession


class Fortnite:
    def __init__(self):
        self.api_url = 'https://fortnite-api.com/v1/stats/br/v2?name='
        self.stats = {
            "duo": {
                "wins": 0,
                "top5": 0,
                "top12": 0,
            },
            "trio": {
                "wins": 0,
                "top3": 0,
                "top6": 0,
            },
            "squad": {
                "wins": 0,
                "top3": 0,
                "top6": 0,
            },
        }
        self.wait: Dict[str, Union[float, asyncio.Event]] = {
            "time": 0
        }

    async def fetch_to_cache(self, name):
        if time.time() - self.wait["time"] > 5:
            self.wait["time"] = time.time()
            self.wait["event"] = asyncio.Event()
            async with ClientSession() as session:
                async with session.get(f'{self.api_url}{name}') as response:
                    self.wait["cache"] = await response.json()
                    self.wait["event"].set()
        await self.wait["event"].wait()
        return self.wait["cache"]

    async def fortnite_request(self, squad_type, stat_type, user):
        d = await self.fetch_to_cache(user["fortnite-name"])
        try:
            x = d["data"]["stats"]["all"][squad_type][stat_type] /\
                d["data"]["stats"]["all"][squad_type]["matches"]
            if x > self.stats[squad_type][stat_type]:
                self.stats[squad_type][stat_type] = x
            return d["data"]["stats"]["all"][squad_type][stat_type] / \
                   d["data"]["stats"]["all"][squad_type]["matches"] / \
                   self.stats[squad_type][stat_type]
        except ZeroDivisionError:
            return 0.0

    async def request_duo_wins(self, user):
        return await self.fortnite_request('duo', 'wins', user)

    async def request_duo_top5(self, user):
        return await self.fortnite_request('duo', 'top5', user)

    async def request_duo_top12(self, user):
        return await self.fortnite_request('duo', 'top12', user)

    async def request_trio_wins(self, user):
        return await self.fortnite_request('trio', 'wins', user)

    async def request_trio_top3(self, user):
        return await self.fortnite_request('trio', 'top3', user)

    async def request_trio_top6(self, user):
        return await self.fortnite_request('trio', 'top6', user)

    async def request_squad_wins(self, user):
        return await self.fortnite_request('squad', 'wins', user)

    async def request_squad_top3(self, user):
        return await self.fortnite_request('squad', 'top3', user)

    async def request_squad_top6(self, user):
        return await self.fortnite_request('squad', 'top6', user)

