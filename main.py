import logging as logger
import socketio
import uvicorn
from pydantic import ValidationError
from collections import defaultdict
from src.web.events import ClientEvent, ServerEvent
from src.service.messages import Message
from src.repository.db.data import TOPICS, QUESTIONS
from src.repository.db import crud
from src.schemas.schemas import Game, JoinGame, Answer, Player, Question
from src.service.utils import enter_room, to_dict
from src.schemas.validators import validate


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
        # data.topic_pk

    @classmethod
    def add_to_waiting_room(cls, room_name: str, player: Player):
        for p_list in cls.waiting_rooms.values():
            if player in p_list:
                p_list.remove(player)
        cls.waiting_rooms[room_name].append(player)
        cls.cleanup_wr()
        assert cls.waiting_rooms  # , cls.waiting_rooms


static_files = {'/': 'static/index.html', '/static': './static'}
server = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(server, static_files=static_files)


async def error_handler(sid, exception: ValidationError):
    msg = exception.json()  # exception.errors()
    await server.emit(ServerEvent.Error.VALIDATION, msg, to=sid)

validate_handler = validate(error_handler, validate_return=True)
# validate_handler = partial(validate, error_handler, validate_return=True)


@server.event
async def connect(sid, _):
    data = Message.ON_CONNECT.format(sid=sid)
    await server.send(data, to=sid)
    logger.info(data)


@server.on(ClientEvent.GET_TOPICS)
async def get_topics(sid, _):
    data = to_dict(TOPICS)
    await server.emit(ServerEvent.Game.TOPICS, data, to=sid)
    logger.info(data)


@server.on(ClientEvent.JOIN_GAME)
@validate_handler
async def join_game(sid, data: JoinGame) -> None:
    waiting_room_name = data.topic_pk
    player = Player(sid=sid, name=data.name)
    if player in GameEnv.waiting_rooms[waiting_room_name]:
        return
    GameEnv.add_to_waiting_room(waiting_room_name, player)
    if GameEnv.is_enough_players_in(waiting_room_name):
        players: list[Player] = GameEnv.waiting_rooms.pop(waiting_room_name)
        game = Game(
            uid=await enter_room(server, players),
            questions=await crud.fetch_all(QUESTIONS, topic=data.topic_pk),
            players=players,
        )
        GameEnv.current_games[game.uid] = game
        # TODO: room notification - game start, send game to each player
        # await send('Game started', room=game.uid)
        await server.emit(
            ServerEvent.Game.GAME,
            game.init(),
            room=game.uid,
        )
    else:
        await server.emit(
            ServerEvent.Game.JOINED,
            Message.ADDED_TO_WAITING_ROOM.format(sid=sid),
            to=sid,
        )


@server.on(ClientEvent.ANSWER)
@validate_handler
async def answer(sid, data: Answer) -> None:
    game: Game = GameEnv.current_games.get(data.game_uid)
    if game is None:
        return await server.emit(
            ServerEvent.Error.NOT_FOUND,
            Message.GAME_NOT_FOUND.format(game_uid=data.game_uid),
            to=sid,
        )
    p: Player = await crud.fetch_one(game.players, sid=sid)
    if p is None:
        return await server.emit(
            ServerEvent.Error.NOT_FOUND,
            Message.PLAYER_NOT_FOUND.format(sid=sid),
            to=sid,
        )
    q: Question = game.questions[p.question_pointer]
    if data.index == q.answer:
        p.score += 1
    p.question_pointer += 1
    if p.question_pointer >= len(game.questions):
        winner: Player = max(game.players, key=lambda x: x.score)
        await server.emit(
            ServerEvent.Game.OVER.format(name=p.name),
            Message.GAME_OVER.format(player=winner.name),
            room=game.uid,
        )
        for p in game.players:
            await server.disconnect(sid=p.sid)

    for p in game.players:
        data = game.output(p)
        await server.emit(ServerEvent.Game.GAME, data, to=p.sid)


@server.event
async def disconnect(sid):
    logger.info(f"Пользователь {sid} отключился")


if __name__ == '__main__':
    uvicorn.run(app)
