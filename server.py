from aiohttp import web
import aiohttp_cors

async def index():
    # TODO
    pass


async def chat_get_handler():
    # TODO
    pass


async def chat_post_handler():
    # TODO
    pass


async def websocket_handler(request):
    # TODO
    pass


# 웹 애플리케이션 관련 설정
app     = web.Application()                 # aiohttp 웹 애플리케이션 생성 및 할당
routes  = [
    web.get('/', index),                    # 사용자에게 보여지는 웹 브라우저
    web.get('/chat', chat_get_handler),     # Chating 핸들러 (GET)
    web.post('/chat', chat_post_handler),   # Chating 핸들러 (POST)
    web.get('/ws', websocket_handler),      # WebSocket 핸들러
]
app.add_routes(routes)                      # 웹 애플리케이션 route 등록
app['websockets'] = set()                   # 웹 소켓 클라이언트 집합 생성


# CORS 설정
cors = aiohttp_cors.setup(app)
for route in list(app.router.routes()):
    cors.add(route)


# 서버 실행
if __name__ == '__main__':
    web.run_app(app)
