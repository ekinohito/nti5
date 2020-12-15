import asyncio
import time
import os
from typing import Dict, Union

from aiohttp import ClientSession


STEAM_URL = "http://steamcommunity.com"
STEAM_API_URL = "http://api.steampowered.com"

PATH_TO_STEAMAPI_KEY = "steam_api_key.txt"


class Payday2:

    def __init__(self):
        self.api_key = open(PATH_TO_STEAMAPI_KEY, mode="r").read()
        # self.api_key = os.getenv("STEAM_API_KEY")
        self.api_url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/" \
                       f"?appid=218620&key={self.api_key}&steamid="

        self.stats = {
            "heist_success": 0,
            "heist_failed": 0,
            "player_level": 0,
            "player_coins": 0,
            "difficulty_bonus": 0,
            "level_help": 0,
            "job_help": 0,
            "heist_winrate": 0,
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

    async def payday2_request(self, stat_name, user):
        d = await self.fetch_to_cache(user["steamid64"])
        for stat in d["playerstats"]["stats"]:
            if stat["name"] == stat_name:
                self.stats[stat_name] = stat["value"]
                break
        return self.stats[stat_name]

    async def request_heist_success(self, user):
        return await self.payday2_request("heist_success", user)

    async def request_heist_failed(self, user):
        return await self.payday2_request("heist_failed", user)

    async def request_player_level(self, user):
        return await self.payday2_request("player_level", user)

    async def request_player_coins(self, user):
        return await self.payday2_request("player_coins", user)

    async def request_difficulty_bonus(self, user):
        self.stats["difficulty_bonus"] = await self.payday2_request("difficulty_normal", user)
        self.stats["difficulty_bonus"] += 2 * await self.payday2_request("difficulty_hard", user)
        self.stats["difficulty_bonus"] += 3 * await self.payday2_request("difficulty_overkill", user)
        return self.stats["difficulty_bonus"]

    async def request_level_help(self, user):
        return await self.payday2_request("level_help", user)

    async def request_job_help(self, user):
        return await self.payday2_request("job_help", user)

    async def request_heist_winrate(self, user):
        try:
            return await self.request_heist_success(user) / await self.request_heist_failed(user)
        except ZeroDivisionError:
            return 0.0
