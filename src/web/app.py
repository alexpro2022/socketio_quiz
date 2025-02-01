import logging as logger

import socketio

from src.pydantic.schemas import Answer, JoinGame
from src.pydantic.validators import ValidationError, validate
from src.repository.db.data import TOPICS
from src.service.game import GameEnv
from src.service.messages import Message
from src.service.utils import to_dict

# from src.web.app import server
from src.web.events import ClientEvent, ServerEvent

static_files = {"/": "static/index.html", "/static": "./static"}
server = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
# logger=True, engineio_logger=True)
app = socketio.ASGIApp(server, static_files=static_files)


async def error_handler(sid, exception: ValidationError):
    msg = exception.json()  # exception.errors()
    await server.emit(ServerEvent.Error.VALIDATION, msg, to=sid)


validate_handler = validate(error_handler, validate_return=True)
# validate_handler = partial(validate, error_handler, validate_return=True)


@server.event
async def connect(sid, _):
    out_data = Message.ON_CONNECT.format(sid=sid)
    await server.send(out_data, to=sid)
    logger.info(out_data)


@server.on(ClientEvent.GET_TOPICS)
async def get_topics(sid, _):
    out_data = to_dict(TOPICS)
    await server.emit(ServerEvent.Game.TOPICS, out_data, to=sid)
    logger.info(out_data)


@server.on(ClientEvent.JOIN_GAME)
@validate_handler
async def join_game(sid, data: JoinGame) -> None:
    out_data = await GameEnv.join_game(sid, data)
    if out_data is not None:
        await server.emit(**out_data.model_dump())
    logger.info(out_data)


@server.on(ClientEvent.ANSWER)
@validate_handler
async def answer(sid, data: Answer) -> None:
    out_data = await GameEnv.answer(sid, data)
    for item in out_data:
        await server.emit(**item.model_dump())
        logger.info(item)


@server.event
async def disconnect(sid):
    logger.info(f"Пользователь {sid} отключился")
