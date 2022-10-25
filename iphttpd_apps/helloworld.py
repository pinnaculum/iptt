from aiohttp import web


async def tell_me(request):
    data = await request.post()

    if data and 'message' in data:
        return web.Response(
            text=data['message']
        )
    else:
        return web.Response(text='What ?')


async def hello_world(request):
    return web.Response(text='Hello world')


async def create_app(args):
    app = web.Application()
    app.add_routes([web.get('/', hello_world)])
    app.add_routes([web.post('/tellme', tell_me)])
    return app
