import asyncio
import time
import os
from typing import Dict, Union
import logging as log

log.basicConfig(level="ERROR")

from aiohttp import ClientSession


STEAM_URL = "http://steamcommunity.com"
STEAM_API_URL = "http://api.steampowered.com"

PATH_TO_STEAMAPI_KEY = "steam_api_key.txt"


max_stats = {
            "total_time_played": 0,
            "total_wins": 0,
            "total_rounds_played": 0,
            "total_mvps": 0,
            "total_matches_won": 0,
            "total_matches_played": 0,
            "total_weapons_donated": 0,
        }


class Csgo:

    def __init__(self):
        self.api_key = open(PATH_TO_STEAMAPI_KEY, mode="r").read()
        # self.api_key = os.getenv("STEAM_API_KEY")
        self.api_url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/" \
                       f"?appid=730&key={self.api_key}&steamid="

        self.stats = {
            "total_time_played": 0,
            "total_wins": 0,
            "total_rounds_played": 0,
            "total_mvps": 0,
            "total_matches_won": 0,
            "total_matches_played": 0,
            "total_weapons_donated": 0,
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


    async def csgo_request(self, stat_name, user):
        # d = await self.fetch_to_cache(user["steamid64"])
        async with ClientSession() as session:
            async with session.get(f'{self.api_url}{user["steamid64"]}') as response:
                d = await response.json()
        # d = await ClientSession().get(f'{self.api_url}{user["steamid64"]}').json()
        log.debug(f"KEK: {stat_name}: {d}")
        for stat in d["playerstats"]["stats"]:
            if stat["name"] == stat_name:
                try:
                    max_stats[stat_name] = max(max_stats[stat_name], stat["value"])
                    self.stats[stat_name] = stat["value"] / max_stats[stat_name]
                except ZeroDivisionError:
                    self.stats[stat_name] = 0
                break
        return self.stats[stat_name]


    async def request_total_time_played(self, user):
        return await self.csgo_request("total_time_played", user)


    async def request_total_wins(self, user):
        return await self.csgo_request("total_wins", user)


    async def request_total_rounds_played(self, user):
        return await self.csgo_request("total_rounds_played", user)


    async def request_total_mvps(self, user):
        return await self.csgo_request("total_mvps", user)


    async def request_total_matches_won(self, user):
        return await self.csgo_request("total_matches_won", user)


    async def request_total_matches_played(self, user):
        return await self.csgo_request("total_matches_played", user)


    async def request_total_weapons_donated(self, user):
        return await self.csgo_request("total_weapons_donated", user)


    async def request_matches_winrate(self, user):
        try:
            return await self.request_total_matches_won(user) / \
                   await self.request_total_matches_played(user)
        except ZeroDivisionError:
            return 0.0


    async def request_rounds_winrate(self, user):
        try:
            return await self.request_total_wins(user) / \
                   await self.request_total_rounds_played(user)
        except ZeroDivisionError:
            return 0.0


    async def request_avg_round_per_match(self, user):
        try:
            return await self.request_total_rounds_played(user) / \
                   await self.request_total_matches_played(user)
        except ZeroDivisionError:
            return 0.0


    async def request_avg_won_round_per_match(self, user):
        try:
            return await self.request_total_wins(user) / \
                   await self.request_total_matches_won(user)
        except ZeroDivisionError:
            return 0.0
