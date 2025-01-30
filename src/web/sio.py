import logging as logger
from src.web.events import ClientEvent, ServerEvent
from src.service.messages import Message
from src.repository.db.data import TOPICS
from src.repository.db import crud
from src.pydantic.schemas import JoinGame, Answer, Player, Question
from src.pydantic.types import GameType, PlayerType
from src.pydantic.validators import validate_handler
from src.service.game import GameEnv
from src.service.utils import to_dict
from src.web.app import server


@server.event
async def connect(sid, *_):
    data = Message.ON_CONNECT.format(sid=sid)
    await server.send(data, to=sid)
    logger.info(data)


@server.on(ClientEvent.GET_TOPICS)
async def get_topics(sid, *_):
    data = to_dict(TOPICS)
    await server.emit(ServerEvent.Game.TOPICS, data, to=sid)
    logger.info(data)


@server.on(ClientEvent.JOIN_GAME)
@validate_handler
async def join_game(sid, data: JoinGame) -> None:
    waiting_room_name = data.topic_pk
    player = Player(sid=sid, name=data.name)
    if player not in GameEnv.waiting_rooms[waiting_room_name]:
        GameEnv.add_to_waiting_room(waiting_room_name, player)
        if GameEnv.is_enough_players_in(waiting_room_name):
            game = await GameEnv.start_game(waiting_room_name)
            await server.emit(
                event=ServerEvent.Game.GAME,
                data=game.init(),
                room=game.uid,
            )
        else:
            await server.emit(
                event=ServerEvent.Game.JOINED,
                data=Message.ADDED_TO_WAITING_ROOM.format(sid=sid),
                to=sid,
            )


@server.on(ClientEvent.ANSWER)
@validate_handler
async def answer(sid, data: Answer) -> None:
    game: GameType = GameEnv.current_games.get(data.game_uid)
    if game is None:
        return await server.emit(
            event=ServerEvent.Error.NOT_FOUND,
            data=Message.GAME_NOT_FOUND.format(game_uid=data.game_uid),
            to=sid,
        )
    p: PlayerType = await crud.fetch_one(game.players, sid=sid)
    if p is None:
        return await server.emit(
            event=ServerEvent.Error.NOT_FOUND,
            data=Message.PLAYER_NOT_FOUND.format(sid=sid),
            to=sid,
        )
    q: Question = game.questions[p.question_pointer]
    if data.index == q.answer:
        p.score += 1
    p.question_pointer += 1
    if p.question_pointer >= len(game.questions):
        winner: Player = max(game.players, key=lambda x: x.score)
        await server.emit(
            event=ServerEvent.Game.OVER.format(name=p.name),
            data=Message.GAME_OVER.format(player=winner.name),
            room=game.uid,
        )
        for p in game.players:
            await server.disconnect(sid=p.sid)

    for p in game.players:
        # data = game.output(p)
        await server.emit(
            event=ServerEvent.Game.GAME,
            data=game.output(p),
            to=p.sid,
        )


@server.event
async def disconnect(sid):
    logger.info(f"Пользователь {sid} отключился")
