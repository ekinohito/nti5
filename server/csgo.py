import requests
import json


import logging as log


log: Logger = logging.getLogger(__name__)
logging.baseConfig(level='DEBUG')


STEAM_URL = "http://steamcommunity.com"
STEAM_API_URL = "http://api.steampowered.com"


KEY = open("steam_api_key.txt", mode="r").read()


def get_player_stats_csgo(steamid):
	
	log.debug("In csgo player getter stats")	

	appid = 730

	GET_USERSTATS_FOR_GAME = STEAM_API_URL + f"/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={KEY}&steamid={steamid}"

	try:
		resp = requests.get(GET_USERSTATS_FOR_GAME).json()
	except json.JSONDecodeError as e:
		log.error(f"JSONDecodeError: {e}")
		return {"success": "false"}
	except BaseException as e:
		log.error(f"Some other response parser error: {e}")
		return {"success": "false"}

	try:
		return {"success": "true", 
				"total_time_played": int(resp["playerstats"]["total_time_played"]),
				"total_wins": int(resp["playerstats"]["total_wins"]),
				"total_rounds_played": int(resp["playerstats"]["total_rounds_played"]),
				"total_mvps": int(resp["playerstats"]["total_mvps"]),
				"total_matches_won": int(resp["playerstats"]["total_matches_won"]),
				"total_matches_played": int(resp["playerstats"]["total_matches_played"]),
				"total_weapons_donated": int(resp["playerstats"]["total_weapons_donated"])
			   }
	except BaseException as e:
		log.error(f"Error in returning: {e}")
		return {"success": "false"}
