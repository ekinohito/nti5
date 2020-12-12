from aiohttp import ClientSession


class Fortnite:
    api_url = 'https://fortnite-api.com/v1/stats/br/v2?name='
    stats = {
        "duo.wins": 0,
        "duo.top5": 0,
        "duo.top12": 0,
    }

    @classmethod
    def fortnite_request(cls):
        async def fortnite_request_prototype(user):
            async with ClientSession() as session:
                async with session.get(f'{cls.api_url}{user["fortnite-name"]}') as response:
                    d = await response.json()
                    x = d["data"]["stats"]["all"]["duo"]["wins"] / d["data"]["stats"]["all"]["duo"]["matches"]
                    if x > cls.stats["duo.wins"]:
                        cls.stats["duo.wins"] = x
                    return d["data"]["stats"]["all"]["duo"]["wins"] / \
                           d["data"]["stats"]["all"]["duo"]["matches"] / \
                           cls.stats["duo.wins"]

    @classmethod
    async def request_duo_matches(cls, user):
        async with ClientSession() as session:
            async with session.get(f'{cls.api_url}{user["fortnite-name"]}') as response:
                return (await response.json())["data"]["stats"]["all"]["duo"]["matches"]

    @classmethod
    async def request_duo_wins(cls, user):
        async with ClientSession() as session:
            async with session.get(f'{cls.api_url}{user["fortnite-name"]}') as response:
                d = await response.json()
                x = d["data"]["stats"]["all"]["duo"]["wins"] / d["data"]["stats"]["all"]["duo"]["matches"]
                if x > cls.stats["duo.wins"]:
                    cls.stats["duo.wins"] = x
                return d["data"]["stats"]["all"]["duo"]["wins"] /\
                       d["data"]["stats"]["all"]["duo"]["matches"] /\
                       cls.stats["duo.wins"]

    @classmethod
    async def request_duo_top5(cls, user):
        async with ClientSession() as session:
            async with session.get(f'{cls.api_url}{user["fortnite-name"]}') as response:
                d = await response.json()
                x = d["data"]["stats"]["all"]["duo"]["top5"] / d["data"]["stats"]["all"]["duo"]["matches"]
                if x > cls.stats["duo.top5"]:
                    cls.stats["duo.wins"] = x
                return d["data"]["stats"]["all"]["duo"]["wins"] /\
                       d["data"]["stats"]["all"]["duo"]["matches"] /\
                       cls.stats["duo.wins"]
