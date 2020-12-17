async def cors_middleware(app, handler):
    async def middleware(request):
        response = await handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        print(response.headers)
        return response
    return middleware
