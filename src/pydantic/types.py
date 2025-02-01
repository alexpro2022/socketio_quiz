from typing import TypeAlias

import socketio

from src.pydantic import schemas

PlayerType: TypeAlias = schemas.Player
GameType: TypeAlias = schemas.Game
ServerType: TypeAlias = socketio.AsyncServer
