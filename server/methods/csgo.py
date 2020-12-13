import asyncio
import random
import time
from typing import Dict, Union

from aiohttp import ClientSession


STEAM_URL = "http://steamcommunity.com"
STEAM_API_URL = "http://api.steampowered.com"

PATH_TO_STEAMAPI_KEY = "steam_api_key.txt"

# def get_player_stats_csgo(steamid):
	
# 	log.debug("In csgo player getter stats")	

# 	appid = 730

# 	GET_USERSTATS_FOR_GAME = STEAM_API_URL + f"/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={KEY}&steamid={steamid}"

# 	try:
# 		resp = requests.get(GET_USERSTATS_FOR_GAME).json()
# 	except json.JSONDecodeError as e:
# 		log.error(f"JSONDecodeError: {e}")
# 		return {"success": "false"}
# 	except BaseException as e:
# 		log.error(f"Some other response parser error: {e}")
# 		return {"success": "false"}

# 	try:
# 		return {"success": "true", 
# 				"total_time_played": int(resp["playerstats"]["total_time_played"]),
# 				"total_wins": int(resp["playerstats"]["total_wins"]),
# 				"total_rounds_played": int(resp["playerstats"]["total_rounds_played"]),
# 				"total_mvps": int(resp["playerstats"]["total_mvps"]),
# 				"total_matches_won": int(resp["playerstats"]["total_matches_won"]),
# 				"total_matches_played": int(resp["playerstats"]["total_matches_played"]),
# 				"total_weapons_donated": int(resp["playerstats"]["total_weapons_donated"])
# 			   }
# 	except BaseException as e:
# 		log.error(f"Error in returning: {e}")
# 		return {"success": "false"}


class Csgo:

	def __init__(self):
		self.api_key = open(PATH_TO_STEAMAPI_KEY, mode="r").read()

		self.api_url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={api_key}&steamid="
		
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


    async def csgo_request(self, stat_type, user):
    	d = await self.fetch_to_cache(user["csgo-steamid64"])
    	self.stats[stat_type] = d["playerstats"][stat_type]


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

