from methods.league_of_legends import LeagueOfLegends
import asyncio

from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = Path(__file__).parent.parent / '.env'
print(str(env_path))
load_dotenv(dotenv_path=env_path)


class TestMethods:
    @staticmethod
    async def test(user):
        return 1

    @staticmethod
    async def test_lol(nickname='frakexx'):
        lol = await LeagueOfLegends().init(summoner_name=nickname)
        stats = await lol.stats_to_cache()


if __name__ == '__main__':
    asyncio.run(TestMethods.test_lol())
