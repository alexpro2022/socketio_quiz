from uuid import uuid4, UUID
from pydantic import BaseModel
import socketio
from src.schemas.schemas import Player


async def enter_room(
    sio: socketio.AsyncServer,
    players: list[Player],
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


def to_dict(items: list[BaseModel]) -> list[dict]:
    return [item.model_dump() for item in items]


def to_json(items: list[BaseModel]) -> list[dict]:
    return [item.model_dump_json() for item in items]


def info(*msg):
    from pprint import pprint
    for item in msg:
        print('=' * 20)
        pprint(item)
    assert 0, msg
