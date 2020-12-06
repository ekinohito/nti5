from aiohttp import web
from sqlalchemy import create_engine
import json


async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))


async def get_games(request):
    response_obj = [
            {
                'title': "Dota 2",
                'description': "Компьютерная многопользовательская командная игра в жанре MOBA",
                'points': "0.456",
                'presented': True,
            },
            {
                'title': "CS:GO",
                'description': "Компьютерная многопользовательская командная игра в жанре FPS",
                'points': "0.567",
                'presented': True,
            },
            {
                'title': "Fortnite",
                'description': "Компьютерная многопользовательская командная игра в жанре BR",
                'points': "0.345",
                'presented': False,
            },
        ]
    return web.Response(text=json.dumps(response_obj))


def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/games', get_games)

    web.run_app(app, port=3010)


if __name__ == '__main__':
    main()
