from aiohttp import web
import utils

from db_base import Base, engine
from methods import LeagueOfLegends
from middlewares import auth_middleware, cors_middleware
from services import UserService

from dotenv import load_dotenv
load_dotenv()


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


def main():
    Base.metadata.create_all(bind=engine)

    app = web.Application(middlewares=[auth_middleware, cors_middleware])
    app.router.add_get('/', handle)
    app.router.add_get('/games', get_games)
    # app.router.add_options('/games', options)
    app.router.add_post('/user/register', register)
    app.router.add_post('/user/login', login)
    app.router.add_post('/games/{game_name}/name', set_games_name)

    web.run_app(app, host='0.0.0.0', port=3010)


if __name__ == '__main__':
    main()
