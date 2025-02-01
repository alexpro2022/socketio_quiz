import socketio

from src.web.sio import server

app = socketio.ASGIApp(
    server, static_files={"/": "static/index.html", "/static": "./static"}
)
