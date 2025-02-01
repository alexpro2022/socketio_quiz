from functools import wraps
from uuid import UUID, uuid4

import socketio

from pydantic import BaseModel
from src.pydantic.types import PlayerType


async def enter_room(
    sio: socketio.AsyncServer,
    players: list[PlayerType],
) -> UUID:
    async def leave_all_rooms(sid):
        _, *rooms = sio.rooms(sid)
        for room in rooms:
            await sio.leave_room(sid, room)

    room = uuid4()
    for player in players:
        await leave_all_rooms(player.sid)
        await sio.enter_room(player.sid, room)
    return room


def to_tuple(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        return res if isinstance(res, (tuple, list)) else [res]

    return wrapper


def to_dict(items: list[BaseModel]) -> list[dict]:
    return [item.model_dump() for item in items]


def to_json(items: list[BaseModel]) -> list[dict]:
    return [item.model_dump_json() for item in items]
