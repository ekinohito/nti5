import asyncio
import json

from aiohttp_middlewares import cors_middleware
from aiohttp import web
import utils

from db_base import Base, engine
from methods import LeagueOfLegends
from middlewares import auth_middleware
from services import UserService

from dotenv import load_dotenv

from tree.tree import TreeDecoder

load_dotenv()

with open('tree/tree.json') as f:
    tree = json.load(f, cls=TreeDecoder)


async def handle(request):
    response_obj = {'status': 'success'}
    return utils.json_response(response_obj)


async def options(request):
    return web.Response(headers={
        'Allow': 'OPTIONS, GET, HEAD',
        "Access-Control-Allow-Origin": "*"
    })


async def get_games(request):

    response_obj = [
            {
                'title': "League of Legends ",
                'description': "Cтратегическая кооперативная игра, в которой две команды из пяти могущественных чемпионов сражаются друг с другом, пытаясь уничтожить вражескую базу",
                'points': "0.456",
                'presented': True,
                'auth': "/lol_auth"
            },
            {
                'title': "CS:GO",
                'description': "Компьютерная многопользовательская командная игра в жанре FPS",
                'points': "0.567",
                'presented': False,
                'auth': "/csgo_auth"
            },
            {
                'title': "Fortnite",
                'description': "Компьютерная многопользовательская командная игра в жанре BR",
                'points': await tree.desc[2].evaluate({"fortnite-name": "100"}),
                'presented': True,
                'auth': "/fortnite_auth"
            },
            {
                'title': "Payday 2",
                'description': "Компьютерная многопользовательская командная игра в жанре FPS",
                'points': "0.567",
                'presented': False,
                'auth': "/pd2_auth"
            },
        ]
    return utils.json_response(response_obj)




async def register(request):
    data = await request.json()

    username, password = data['username'], data['password']

    if UserService.get_user(username=username):
        return utils.json_response({
            "errors": [
                {"username": "exists"}
            ]
        })

    user = UserService.add_user(username, password)

    return web.Response(text=utils.create_jwt_token(user.id))


async def login(request):
    data = await request.json()

    username, password = data['username'], data['password']
    user = UserService.get_user(username=username)

    if not user:
        return utils.json_response({
            "errors": [
                {"username": "not exists"}
            ]
        })
    else:
        if user.password == password:
            return web.Response(text=utils.create_jwt_token(user.id))
        return utils.json_response({
            "errors": [
                {"password": "incorrect"}
            ]
        })


async def get_user(request):
    return utils.json_response({
        'username': request.user.username,
        'lol_nickname': request.user.lol_nickname
    })





async def set_games_name(request):
    if not request.user:
        return web.Response(status=401)
    game_name = request.match_info.get('game_name')

    data = await request.json()
    payload = data["payload"]
    if game_name == 'lol':
        account_id = (await LeagueOfLegends().init(summoner_name=payload)).account_id
        UserService.update_games(request.user.id, lol_account_id=account_id, lol_nickname=payload)
        return web.Response(status=200)
    elif game_name == 'csgo':
        UserService.update_games(request.user.id, steam_id=payload)


async def csgo_auth(request):
    if not request.user:
        return web.Response(status=401)

    data = request.json()

    UserService.update_games(request.user.id, steam_id=data['steamid64'])
    return web.Response(status=200)


async def pd2_auth(request):
    if not request.user:
        return web.Response(status=401)

    data = request.json()

    UserService.update_games(request.user.id, steam_id=data['steamid64'])
    return web.Response(status=200)


async def lol_auth(request):
    if not request.user:
        return web.Response(status=401)

    data = request.json()

    UserService.update_games(request.user.id, lol_account_id=data['account_id'],
                             lol_nickname=data['lol_nickname'])
    return web.Response(status=200)


async def fortnite_auth(request):
    if not request.user:
        return web.Response(status=401)

    data = request.json()

    UserService.update_games(request.user.id, fortnite_id=data['fortnite_id'])
    return web.Response(status=200)



def main():
    Base.metadata.create_all(bind=engine)

    app = web.Application(middlewares=[cors_middleware(origins=['http://localhost:3000']), auth_middleware])
    app.router.add_get('/', handle)
    app.router.add_get('/games', get_games)
    # app.router.add_options('/games', options)
    app.router.add_get('/user', get_user)
    app.router.add_post('/user/register', register)
    app.router.add_post('/user/login', login)
    app.router.add_post('/games/{game_name}/name', set_games_name)

    app.router.add_post('/csgo_auth', csgo_auth)
    app.router.add_post('/pd2_auth', pd2_auth)
    app.router.add_post('/lol_auth', lol_auth)
    app.router.add_post('/fortnite_auth', fortnite_auth)

    web.run_app(app, host='0.0.0.0', port=3010)


if __name__ == '__main__':
    main()
