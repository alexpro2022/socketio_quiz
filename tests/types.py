from typing import Any, TypeAlias

import socketio

from src.pydantic.types import PlayerType  # noqa

ClientType: TypeAlias = socketio.AsyncSimpleClient  # AsyncClient
ClientsType: TypeAlias = list[ClientType]
DataType: TypeAlias = Any | None
EventType: TypeAlias = Any
ResponseType: TypeAlias = tuple | list
RoomType: TypeAlias = str
