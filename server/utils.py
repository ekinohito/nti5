import json
import os

import jwt
from aiohttp import web


def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    kwargs['headers'] = {"Access-Control-Allow-Origin": "*"}
    return web.Response(**kwargs)


def create_jwt_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        # 'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, os.getenv('JWT_SECRET'), os.getenv('JWT_ALGORITHM'))
    return jwt_token.decode('utf-8')
