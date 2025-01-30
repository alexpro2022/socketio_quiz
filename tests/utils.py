from typing import Callable
import pytest
import socketio
import socketio.exceptions
from src.service.game import GameEnv
from src.service.messages import Message
from src.web.events import ClientEvent, ServerEvent
from src.pydantic.schemas import JoinGame, Game, Player, NonNegativeInt
from .conftest import AppTest
from .types import (
    ClientType, ClientsType, DataType, EventType, PlayerType, ResponseType
)

waiting_rooms = GameEnv.waiting_rooms


def raise_assert(msg: str) -> None:
    assert 0, msg


async def emit_receive(
    entity: ClientType | ClientsType,
    event: EventType,
    data: DataType = None,
    timeout=AppTest.timeout,
    room: bool = False,
    compare_responses: bool = True,
) -> ResponseType | tuple[ResponseType]:

    class ErrorMessage:
        WRONG_TYPE = f'=== Wrong type `{type(entity)}`'
        BROADCAST = 'Event `{event}`: argument `{arg}` is missing, server is broadcasting instead'
        ROOM_MISS = 'Event `{event}`: argument `room=` is missing, argument `to=sid` is used instead'
        DIFF_EVENT = 'Different events for users in room'
        DIFF_DATA = 'Different data for users in room'

    async def emit_receive_to_sid():
        if isinstance(entity, (tuple, list)):
            active, *passive = entity
        elif isinstance(entity, ClientType):
            active, passive = entity, []
        else:
            raise_assert(ErrorMessage.WRONG_TYPE)
        await active.emit(event, data or {})
        for item in passive:
            with pytest.raises(socketio.exceptions.TimeoutError):
                r = await item.receive(timeout)
                raise_assert(ErrorMessage.BROADCAST.format(event=r[0], arg='to=sid'))
        return await active.receive(timeout)

    async def emit_receive_to_room():
        active, passive, outside_user = entity
        await active.emit(event, data or {})
        with pytest.raises(socketio.exceptions.TimeoutError):
            r = await outside_user.receive(timeout)
            raise_assert(ErrorMessage.BROADCAST.format(event=r[0], arg='room='))
        active_response = await active.receive(AppTest.timeout)
        try:
            passive_response = await passive.receive(AppTest.timeout)
        except socketio.exceptions.TimeoutError:
            raise_assert(ErrorMessage.ROOM_MISS.format(event=event))
        if compare_responses:
            assert active_response[0] == passive_response[0], ErrorMessage.DIFF_EVENT
            assert active_response[1] == passive_response[1], ErrorMessage.DIFF_DATA
            return active_response
        return active_response, passive_response

    return await emit_receive_to_room() if room else await emit_receive_to_sid()


def check_response(
    response: ResponseType,
    expected_event: EventType,
    expected_data: DataType = None,
    check_data_func: Callable | None = None
) -> None:
    event, data = response
    assert event == expected_event, event
    if expected_data is not None:
        assert data == expected_data, data
    if check_data_func is not None:
        check_data_func(data)


def check_client_rooms(
    server: socketio.AsyncServer,
    client: ClientType,
    expected_rooms: list[str],
) -> None:
    sid, *rooms = server.rooms(client.sid)
    assert sid == client.sid
    assert rooms == expected_rooms, rooms


def check_waiting_players_amount(
    expected_amount: int,
) -> None:
    assert waiting_rooms, waiting_rooms
    amount = sum(map(len, waiting_rooms.values()))
    assert amount == expected_amount, amount


def check_waiting_player(
    expected_sid: str,
    game_data: JoinGame,
) -> None:
    assert waiting_rooms
    waiting_player: PlayerType = waiting_rooms[game_data.topic_pk][0]
    assert waiting_player.sid == expected_sid, waiting_player.sid
    assert waiting_player.name == game_data.name, waiting_player.name


async def check_join_game_event(
    clients: ClientsType,
    game_data: JoinGame,
) -> None:
    check_response(
        response=await emit_receive(
            clients, ClientEvent.JOIN_GAME, game_data.model_dump()
        ),
        expected_event=ServerEvent.Game.JOINED,
        expected_data=Message.ADDED_TO_WAITING_ROOM.format(
            sid=clients[0].sid
        ),
    )
    assert GameEnv.waiting_rooms


def get_current_game(
    current_games: dict,
) -> Game:
    game_uid, game = list(current_games.items())[0]
    # return Game.model_validate(game)
    assert game_uid == game.uid, game_uid
    assert game is Game.model_validate(game)
    return game


def get_valid_data(
    index: int = 0,
    current_games: dict = GameEnv.current_games,
) -> dict:
    return dict(
        index=index,
        game_uid=str(get_current_game(current_games).uid)
    )


def check_game_data(
    player: Player,
    expected_score: NonNegativeInt,
    expected_question_pointer: NonNegativeInt,
):
    assert player.score == expected_score, player.score
    assert player.question_pointer == expected_question_pointer, \
        player.question_pointer
