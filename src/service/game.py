from collections import defaultdict
from src.pydantic.schemas import Game
from src.pydantic.types import GameType, PlayerType
from src.repository.db import crud, data
from src.service.utils import enter_room
from src.web.app import server


class GameEnv:
    """Game environment."""
    USERS_AMOUNT_FOR_GAME = 2
    waiting_rooms = defaultdict(list)
    current_games = {}

    @classmethod
    def cleanup_wr(cls) -> None:
        to_be_deleted = [k for k, v in cls.waiting_rooms.items() if not v]
        for k in to_be_deleted:
            cls.waiting_rooms.pop(k)
        assert all(cls.waiting_rooms.values())

    @classmethod
    def is_enough_players_in(cls, room_name: str) -> bool:
        return len(cls.waiting_rooms[room_name]) == cls.USERS_AMOUNT_FOR_GAME

    @classmethod
    def add_to_waiting_room(cls, room_name: str, player: PlayerType) -> None:
        for p_list in cls.waiting_rooms.values():
            if player in p_list:
                p_list.remove(player)
        cls.waiting_rooms[room_name].append(player)
        cls.cleanup_wr()
        assert cls.waiting_rooms, cls.waiting_rooms

    @classmethod
    async def start_game(cls, waiting_room_name: str) -> GameType:
        players: list[PlayerType] = GameEnv.waiting_rooms.pop(waiting_room_name)
        game = Game(
            uid=await enter_room(server, players),
            questions=await crud.fetch_all(data.QUESTIONS, topic=waiting_room_name),
            players=players,
        )
        GameEnv.current_games[game.uid] = game
        return game
