from typing import Any, TypeAlias
import socketio

from src.schemas.schemas import Player

ClientType: TypeAlias = socketio.AsyncSimpleClient  # AsyncClient
ClientsType: TypeAlias = list[ClientType]
DataType: TypeAlias = Any | None
EventType: TypeAlias = Any
PlayerType: TypeAlias = Player
ResponseType: TypeAlias = tuple | list
RoomType: TypeAlias = str
