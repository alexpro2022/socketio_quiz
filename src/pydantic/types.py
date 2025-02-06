from typing import TypeAlias

import socketio

from pydantic import BaseModel
from src.pydantic import schemas

ModelType: TypeAlias = BaseModel
SeqType: TypeAlias = list[ModelType]
PlayerType: TypeAlias = schemas.Player
GameType: TypeAlias = schemas.Game
ServerType: TypeAlias = socketio.AsyncServer
