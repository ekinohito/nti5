import os

import jwt
from aiohttp.web_response import json_response

from services import UserService


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        authorization = request.headers.get('authorization', None)
        print(authorization)
        if authorization:
            try:
                jwt_token = authorization.split()[1]
                payload = jwt.decode(jwt_token, os.getenv('JWT_SECRET'),
                                     algorithms=[os.getenv('JWT_ALGORITHM')])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response({'message': 'Token is invalid'}, status=400)

            user = UserService.get_user(payload['user_id'])
            request.user = user
        return await handler(request)
    return middleware
