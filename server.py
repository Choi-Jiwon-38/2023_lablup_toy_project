from aiohttp import web
import aiohttp_session
from aiohttp_session import get_session
import uuid


async def index(request):               # '/'에 대한 GET 요청 발생 시 실행
    f = open('./template/index.html')   # template 디렉토리의 index.html 파일을 읽은 뒤, f에 파일 객체 할당
    session         = await get_session(request)
    session['id']   = str(uuid.uuid4())

    # 세션 ID를 함께 return하는 web.Response 객체 생성
    response = web.Response(text=f.read(), content_type='text/html')
    response.set_cookie('sessionId', session['id' ])

    return response


async def websocket_handler(request):
    app = request.app
    ws  = web.WebSocketResponse()
    await ws.prepare(request)
    session = await get_session(request)

    app['websockets'].add(ws)

    try:
        async for message in ws:
            for client in app['websockets']:
                await client.send_json({'id': session['id'], 'message': message.data})
    finally:
        app['websockets'].remove(ws)

    return ws


async def init_app():                               # 웹 애플리케이션 관련 설정
    app     = web.Application()                     # aiohttp 웹 애플리케이션 생성 및 할당
    routes  = [
        web.get('/', index),                        # 사용자에게 보여지는 웹 브라우저
        web.get('/ws', websocket_handler),          # WebSocket 핸들러
    ]
    app.add_routes(routes)                          # 웹 애플리케이션 route 등록
    app['websockets']   = set()                     # 웹 소켓 클라이언트 집합 생성

    # 브라우저 세션 설정 (브라우저 세션마다 고유 id 할당 목적)
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())

    return app


# 서버 실행
if __name__ == '__main__':
    web.run_app(init_app())
