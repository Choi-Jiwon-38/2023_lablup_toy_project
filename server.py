from aiohttp import web
import aiohttp_cors
import redis.asyncio as redis
import asyncio
import async_timeout
import aiohttp_session
from aiohttp_session import get_session
import uuid

async def index(request):               # '/'에 대한 GET 요청 발생 시 실행
    f = open('./template/index.html')   # template 디렉토리의 index.html 파일을 읽은 뒤, f에 파일 객체 할당
    session         = await get_session(request)
    session['id']   = str(uuid.uuid4())
    print(session['id'])

    # 세션 ID를 함께 return하는 web.Response 객체 생성
    response = web.Response(text=f.read(), content_type='text/html')
    response.set_cookie('sessionId', session['id' ])

    return response


async def chat_get_handler(request):
    redis_pubsub = request.app['pubsub']

    while True:
        try:
            async with async_timeout.timeout(1):
                message = await redis_pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(message['data'].decode())
                break
        except asyncio.TimeoutError:
            pass



async def chat_post_handler(request, message):
    redis_client = request.app['redis']
    await redis_client.publish('single_room', message)


async def websocket_handler(request):
    app = request.app
    ws  = web.WebSocketResponse()
    await ws.prepare(request)
    session = await get_session(request)

    app['websockets'].add(ws)

    try:
        async for message in ws:
            for client in app['websockets']:
                await chat_post_handler(request, str(message.data))
                await client.send_json({'id': session['id'], 'message': message.data})
    finally:
        app['websockets'].remove(ws)

    return ws


async def init_app():                               # 웹 애플리케이션 관련 설정
    app     = web.Application()                     # aiohttp 웹 애플리케이션 생성 및 할당
    routes  = [
        web.get('/', index),                        # 사용자에게 보여지는 웹 브라우저
        web.get('/chat', chat_get_handler),         # Chating 핸들러 (GET)
        web.post('/chat', chat_post_handler),       # Chating 핸들러 (POST)
        web.get('/ws', websocket_handler),          # WebSocket 핸들러
    ]
    app.add_routes(routes)                          # 웹 애플리케이션 route 등록
    app['websockets']   = set()                     # 웹 소켓 클라이언트 집합 생성
    app['redis']        = await redis.from_url("redis://localhost")
    app['pubsub']       = app['redis'].pubsub()     # redis Publish/Subscribe 메시징을 위하여 할당
    await app['pubsub'].subscribe('single_room')    # single-room 채팅

    # CORS 설정
    cors = aiohttp_cors.setup(app)
    for route in list(app.router.routes()):
        cors.add(route)
    
    # 브라우저 세션 설정 (브라우저 세션마다 고유 id 할당 목적)
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())

    return app


# 서버 실행
if __name__ == '__main__':
    web.run_app(init_app())
