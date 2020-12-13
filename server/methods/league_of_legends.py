from typing import List

from aiohttp import ClientSession


class MatchStats:
    dmg_taken: int
    cc_dealt: int
    dmg_dealt: int
    minions_killed: int
    heal: int
    vision_score: int
    kda: int

    def __init__(self, json, game_duration):
        mins = game_duration / 60

        self.dmg_taken = json['totalDamageTaken'] / mins
        self.cc_dealt = json['totalTimeCrowdControlDealt'] / mins
        self.dmg_dealt = json['totalDamageDealtToChampions'] / mins
        self.minions_killed = json['totalMinionsKilled'] / mins
        self.heal = json['totalHeal'] / mins
        self.vision_score = json['visionScore'] / mins
        self.kda = (json['kills'] + json['assists']) / json['deaths']


class LeagueOfLegends:
    api_url = ''

    @staticmethod
    async def get_account_id(summoner_name) -> int:
        url = f'{LeagueOfLegends.api_url}/lol/summoner/v4/summoners/by-name/{summoner_name}'
        async with ClientSession as session:
            async with session.get(url) as response:
                return (await response.json())['accountId']

    @staticmethod
    async def get_games_stats(account_id, count=20) -> List[MatchStats]:
        matches_url = f'{LeagueOfLegends.api_url}/lol/match/v4/matchlists/by-account/{account_id}'
        match_url = f'{LeagueOfLegends.api_url}/lol/match/v4/matches/%d'
        async with ClientSession as session:
            game_duration: int

            match_id: list
            async with session.get(matches_url) as response:
                json = await response.json()
                game_duration = json['gameDuration']
                match_ids = [i['gameId'] for i in json['matches']][:count]

            match_stats: List[MatchStats] = []
            for i in match_ids:
                async with session.get(match_url % i) as response:
                    match_stats.append(
                        MatchStats([i for i in (await response.json())['participants'] if i['participantId'] == account_id][0], game_duration)
                    )
            return match_stats
