from typing import List

from aiohttp import ClientSession
import os


class LolMatchStats:
    dmg_taken: int
    cc_dealt: int
    dmg_dealt: int
    minions_killed: int
    heal: int
    vision_score: int
    kda: int
    role: str

    def __init__(self, stats, game_duration, role):
        mins = game_duration / 60

        self.dmg_taken = stats['totalDamageTaken'] / mins
        self.cc_dealt = stats['totalTimeCrowdControlDealt'] / mins
        self.dmg_dealt = stats['totalDamageDealtToChampions'] / mins
        self.minions_killed = stats['totalMinionsKilled'] / mins
        self.heal = stats['totalHeal'] / mins
        self.vision_score = stats['visionScore'] / mins
        if stats['deaths']:
            self.kda = (stats['kills'] + stats['assists']) / stats['deaths']
        else:
            self.kda = 1000
        self.role = role


class LeagueOfLegends:
    _api_url: str
    _account_id: int
    stats: List[LolMatchStats]

    async def init(self, summoner_id: int = None, summoner_name: str = None):
        self._api_url = f'https://euw1.api.riotgames.com%s?api_key={os.getenv("LOL_API_KEY")}'
        if summoner_id and not summoner_name:
            self._account_id = summoner_id
        elif not summoner_id and summoner_name:
            self._account_id = await self._get_account_id(summoner_name)
        return self

    async def stats_to_cache(self):
        self.stats = await self._get_games_stats()

    async def _get_account_id(self, summoner_name) -> int:
        url = self._api_url % f'/lol/summoner/v4/summoners/by-name/{summoner_name}'
        async with ClientSession() as session:
            async with session.get(url) as response:
                return (await response.json())['accountId']

    async def _get_games_stats(self, count=20) -> List[LolMatchStats]:
        matches_url = self._api_url % f'/lol/match/v4/matchlists/by-account/{self._account_id}'
        match_url = self._api_url % '/lol/match/v4/matches/%d'
        async with ClientSession() as session:
            matches: list
            async with session.get(matches_url) as response:
                json = await response.json()
                matches = [{'gameId': i['gameId'], 'role': i['role']} for i in json['matches']][:count]

            match_stats: List[LolMatchStats] = []
            k = 0
            for game_obj in matches:
                async with session.get(match_url % game_obj['gameId']) as response:
                    k += 1
                    print(k)
                    json = await response.json()
                    participant_id = [i['participantId'] for i in json['participantIdentities'] if i['player']['accountId'] == self._account_id][0]

                    game_duration = json['gameDuration']
                    match_stats.append(
                        LolMatchStats([i for i in json['participants'] if i['participantId'] == participant_id][0]['stats'], game_duration, game_obj['role'])
                    )
            return match_stats
