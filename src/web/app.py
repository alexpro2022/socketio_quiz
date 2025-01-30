import socketio


static_files = {'/': 'static/index.html', '/static': './static'}
server = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(server, static_files=static_files)
