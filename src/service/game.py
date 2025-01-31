from collections import defaultdict
from uuid import UUID

from src.pydantic.schemas import Answer, Game, JoinGame, Player, Question, ServiceToWeb
from src.pydantic.types import GameType, PlayerType
from src.repository.db import crud, data
from src.service.messages import Message
from src.service.utils import enter_room, to_tuple
from src.web.app import server
from src.web.events import ServerEvent


class GameEnv:
    """Game environment."""

    USERS_AMOUNT_FOR_GAME = 2
    waiting_rooms: dict[int | str, list[PlayerType]] = defaultdict(list)
    current_games: dict[UUID, GameType] = {}

    @classmethod
    def cleanup_wr(cls) -> None:
        to_be_deleted = [k for k, v in cls.waiting_rooms.items() if not v]
        for k in to_be_deleted:
            cls.waiting_rooms.pop(k)
        assert all(cls.waiting_rooms.values())

    @classmethod
    def is_enough_players_in(cls, room_name: int | str) -> bool:
        return len(cls.waiting_rooms[room_name]) == cls.USERS_AMOUNT_FOR_GAME

    @classmethod
    def add_to_waiting_room(cls, room_name: int | str, player: PlayerType) -> None:
        for p_list in cls.waiting_rooms.values():
            if player in p_list:
                p_list.remove(player)
        cls.waiting_rooms[room_name].append(player)
        cls.cleanup_wr()

    @classmethod
    async def start_game(cls, waiting_room_name: int | str) -> GameType:
        players: list[PlayerType] = cls.waiting_rooms.pop(waiting_room_name)
        game = Game(
            uid=await enter_room(server, players),
            questions=await crud.fetch_all(data.QUESTIONS, topic=waiting_room_name),
            players=players,
        )
        cls.current_games[game.uid] = game
        return game

    @classmethod
    async def join_game(cls, sid, data: JoinGame) -> ServiceToWeb | None:
        waiting_room_name = data.topic_pk
        player = Player(sid=sid, name=data.name)
        if player in cls.waiting_rooms[waiting_room_name]:
            return None
        cls.add_to_waiting_room(waiting_room_name, player)
        if cls.is_enough_players_in(waiting_room_name):
            game = await cls.start_game(waiting_room_name)
            return ServiceToWeb(
                event=ServerEvent.Game.GAME,
                data=game.init(),
                room=game.uid,
            )
        return ServiceToWeb(
            event=ServerEvent.Game.JOINED,
            data=Message.ADDED_TO_WAITING_ROOM.format(sid=sid),
            to=sid,
        )

    @classmethod
    @to_tuple
    def answer(cls, sid, data: Answer) -> list[ServiceToWeb]:
        game: GameType | None = cls.current_games.get(data.game_uid)
        if game is None:
            return ServiceToWeb(
                event=ServerEvent.Error.NOT_FOUND,
                data=Message.GAME_NOT_FOUND.format(game_uid=data.game_uid),
                to=sid,
            )
        try:
            p: PlayerType = [p for p in game.players if p.sid == sid][0]
        except IndexError:
            return ServiceToWeb(
                event=ServerEvent.Error.NOT_FOUND,
                data=Message.PLAYER_NOT_FOUND.format(sid=sid),
                to=sid,
            )
        if p.question_pointer < len(game.questions):
            q: Question = game.questions[p.question_pointer]
            if data.index == q.answer:
                p.score += 1
            p.question_pointer += 1
        if p.question_pointer == len(game.questions):
            winner: Player = max(game.players, key=lambda x: x.score)
            return ServiceToWeb(
                event=ServerEvent.Game.OVER.format(name=p.name),
                data=Message.GAME_OVER.format(player=winner.name),
                room=game.uid,
            )
        return [
            ServiceToWeb(
                event=ServerEvent.Game.GAME,
                data=game.output(p),
                to=p.sid,
            )
            for p in game.players
        ]
