from aiohttp import web
import aiohttp_session
from aiohttp_session import get_session
import uuid
import redis.asyncio as redis
import json
import asyncio
from datetime import datetime


redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0)        # Redis pool에 대한 설정

async def index(request):               # '/'에 대한 GET 요청 발생 시 실행
    f = open('./template/index.html')   # template 디렉토리의 index.html 파일을 읽은 뒤, f에 파일 객체 할당
    session         = await get_session(request)
    session['id']   = str(uuid.uuid4())

    # 세션 ID를 함께 return하는 web.Response 객체 생성
    response = web.Response(text=f.read(), content_type='text/html')    # ./template/index.html 파일을 읽어서 web 응답 객체로 만듦
    response.set_cookie('sessionId', session['id' ])                    # web 응답 객체마다 고유 session id를 생성하고 cookie로 부여함

    return response


async def websocket_handler(request):
    app = request.app
    ws  = web.WebSocketResponse()           # websocket 응답 객체 생성 및 할당
    await ws.prepare(request)               # websocket에 요청이 오는 것을 대기
    session = await get_session(request)    # session에 대한 정보를 사용하기 위하여 get

    app['websockets'].add(ws)               # websocket에 연결되어 websockets set에 저장

    async def send_message_to_client(pubsub, clients):
        json_message = await pubsub.get_message('messages')             # message 채널에서 message를 가져옴

        while json_message is None:                                     # redis에 publish 되기까지를 기다림 (publish 이전에 get_message는 None을 반환)
            await asyncio.sleep(0.1)                                    # redis에 publish를 위하여 약간의 time sleeep을 부여
            json_message = await pubsub.get_message('messages')         # get_message() 재시도

        for client in clients:                                          # websocket에 연결되어 있는 client들마다                                          
            await client.send_json(json.loads(json_message['data']))    # message 정보를 json 형태로 전송

    try:
        async for message in ws:
            now = datetime.now()                                # datetime을 이용하여 현재 시간 저장
            data = json.dumps({
                'id'        : session['id'],                    # session의 id (사용자 식별의 용도로 사용)
                'message'   : str(message.data),                # 사용자가 socket을 통해 보낸 message
                'time'      : f'{now.hour}:{now.minute}',       # 메세지 전송 시간
            })
            await app['redis'].publish('messages', data)                                    # message 채널(single-room)에 위에서 정의한 data를 publish
            asyncio.create_task(send_message_to_client(app['pubsub'], app['websockets']))   # client에게 message를 전송하는 작업(redis에서 get -> ws로 전송)을 비동기적으로 처리하기 위하여 create_task 사용

    finally:                                    
        app['websockets'].remove(ws)            # websocket 제거

    return ws


async def init_app():                           # 웹 애플리케이션 관련 설정
    app     = web.Application()                 # aiohttp 웹 애플리케이션 생성 및 할당
    routes  = [
        web.get('/', index),                    # 사용자에게 보여지는 웹 브라우저
        web.get('/ws', websocket_handler),      # WebSocket 핸들러
    ]
    app.add_routes(routes)                      # 웹 애플리케이션 route 등록
    app['websockets']   = set()                 # 웹 소켓 클라이언트 집합 생성
    app['redis']        = redis.Redis(connection_pool=redis_pool)   # Redis pool에 연결된 Redis client 할당
    app['pubsub']       = app['redis'].pubsub()                     # 위 Redis client의 pubsub 객체 할당

    await app['pubsub'].subscribe('messages')                       # single-room이므로 'messages'라는 1개의 채널만 구독함

    # 브라우저 세션 설정 (브라우저 세션마다 고유 id 할당 목적)
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())

    return app


# 서버 실행
if __name__ == '__main__':
    web.run_app(init_app())
