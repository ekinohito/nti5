from aiohttp import ClientSession


class Fortnite:
    api_url = ''

    @staticmethod
    async def request_total_matches(user):
        async with ClientSession as session:
            async with session.get('') as response:
                return await response.json()
