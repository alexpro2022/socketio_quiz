from collections.abc import Callable
from uuid import uuid4

import pytest
from socketio import exceptions

from src.pydantic.schemas import GameOut, JoinGame, Player, QuestionOut
from src.repository.db.data import TOPICS
from src.service.game import GameEnv
from src.service.messages import Message
from src.service.utils import to_dict
from src.web.events import ClientEvent, ServerEvent
from src.web.sio import server

from . import utils as u
from .conftest import AppTest, pytestmark  # noqa
from .types import ClientsType

TOPIC_PK = 5
JOIN_FIRST_PLAYER = JoinGame(topic_pk=TOPIC_PK, name="Alex")
JOIN_SECOND_PLAYER = JoinGame(topic_pk=TOPIC_PK + 1, name="Alice")
waiting_rooms = GameEnv.waiting_rooms
current_games = GameEnv.current_games


async def test__connection(clients: ClientsType):
    for c in clients:
        u.check_response(
            response=await c.receive(AppTest.timeout),
            expected_event=ServerEvent.MESSAGE,
            expected_data=Message.ON_CONNECT.format(sid=c.sid),
        )


async def test__get_topics(clients: ClientsType):
    for clnts in (clients, clients[::-1]):
        u.check_response(
            response=await u.emit_receive(clnts, ClientEvent.GET_TOPICS),
            expected_event=ServerEvent.Game.TOPICS,
            expected_data=to_dict(TOPICS),
        )


@pytest.mark.parametrize(
    "event, invalid_data",
    (
        # join_game
        (ClientEvent.JOIN_GAME, None),
        (ClientEvent.JOIN_GAME, dict(topic_pk=-1, name="name")),
        (ClientEvent.JOIN_GAME, dict(topic_pk=0, name=1)),
        # answer
        (ClientEvent.ANSWER, None),
        (ClientEvent.ANSWER, dict(index=-1, game_uid=str(uuid4()))),
        (ClientEvent.ANSWER, dict(index=0, game_uid="")),
    ),
)
async def test__validation(clients: ClientsType, event, invalid_data):
    u.check_response(
        response=await u.emit_receive(clients, event, invalid_data),
        expected_event=ServerEvent.Error.VALIDATION,
    )


async def test__joined_user_added_to_waiting_room(clients: ClientsType):
    assert not waiting_rooms
    await u.check_join_game_event(clients, JOIN_FIRST_PLAYER)
    assert GameEnv.waiting_rooms
    u.check_waiting_players_amount(1)
    u.check_waiting_player(clients[0].sid, JOIN_FIRST_PLAYER)


async def test__ignore_join_to_same_game(clients: ClientsType):
    """Waiting rooms stay intact, no emit."""
    waiting_rooms_before = waiting_rooms.copy()
    with pytest.raises(exceptions.TimeoutError):
        await u.check_join_game_event(clients, JOIN_FIRST_PLAYER)
    assert waiting_rooms == waiting_rooms_before


async def test__join_only_one_game(clients: ClientsType):
    """When user is joined game and being waiting, but goes back and changes game,
    he should be removed from current waiting room and transferred to another waiting room."""
    topic_before = JOIN_FIRST_PLAYER.topic_pk
    player_before = waiting_rooms[topic_before][0]

    # join_new_game
    JOIN_FIRST_PLAYER.topic_pk += 1
    await u.check_join_game_event(clients, JOIN_FIRST_PLAYER)
    u.check_waiting_players_amount(1)
    u.check_waiting_player(clients[0].sid, JOIN_FIRST_PLAYER)

    # previous game is removed, player moved to new game players list
    assert waiting_rooms.get(topic_before) is None
    assert waiting_rooms[JOIN_FIRST_PLAYER.topic_pk] == [player_before]


async def test__join_game_second_player_starts_game(clients: ClientsType):
    """Second user triggers the game start."""
    waiting_player, new_player, outside_user = clients
    assert not current_games

    # check messages receive two users inside room and not users outside
    players_in_room = (new_player, waiting_player)
    response = await u.emit_receive(
        (*players_in_room, outside_user),
        event=ClientEvent.JOIN_GAME,
        data=JOIN_SECOND_PLAYER.model_dump(),
        room=True,
    )
    u.check_response(
        response=response,
        expected_event=ServerEvent.Game.GAME,
    )
    # check game has been created and saved in repository (dict in memory)
    assert current_games
    assert len(current_games) == 1
    game = u.get_current_game(current_games)
    for p in game.players:
        u.check_game_data(
            player=p,
            expected_score=0,
            expected_question_pointer=0,
        )
    # check game data to be sent to client
    game_out_data = GameOut.model_validate(response[1])
    for p in game_out_data.players:
        assert p.score == 0
    assert game_out_data.question_count == len(game.questions)
    assert game_out_data.current_question == QuestionOut.model_validate(
        game.questions[0]
    )

    # check rooms
    assert not waiting_rooms
    for p in game.players:
        assert server.rooms(p.sid)[1:] == [game.uid]


async def test__answer_game_not_found(clients: ClientsType):
    wrong_game_uid = str(uuid4())
    u.check_response(
        response=await u.emit_receive(
            clients,
            event=ClientEvent.ANSWER,
            data=dict(index=0, game_uid=wrong_game_uid),
        ),
        expected_event=ServerEvent.Error.NOT_FOUND,
        expected_data=Message.GAME_NOT_FOUND.format(game_uid=wrong_game_uid),
    )


async def test__answer_player_not_found(clients: ClientsType):
    outside_user = clients[2]
    u.check_response(
        response=await u.emit_receive(
            clients[::-1],
            event=ClientEvent.ANSWER,
            data=u.get_valid_data(),
        ),
        expected_event=ServerEvent.Error.NOT_FOUND,
        expected_data=Message.PLAYER_NOT_FOUND.format(sid=outside_user.sid),
    )


async def test__answer_emit_to_players_their_data(clients: ClientsType):
    """Clients should receive different response data as per their game progress."""
    game = u.get_current_game(current_games)

    def check_data(player: Player) -> Callable:
        def func(data: GameOut):
            game_out = GameOut.model_validate(data)
            assert game_out.current_question == QuestionOut.model_validate(
                game.questions[player.question_pointer]
            )

        return func

    first_player, second_player = game.players
    # simulate first player one question ahead
    first_player.question_pointer += 1
    first_player_response, second_player_response = await u.emit_receive(
        clients,
        event=ClientEvent.ANSWER,
        data=u.get_valid_data(),
        room=True,
        compare_responses=False,
    )
    u.check_response(
        response=first_player_response,
        expected_event=ServerEvent.Game.GAME,
        check_data_func=check_data(first_player),
    )
    u.check_response(
        response=second_player_response,
        expected_event=ServerEvent.Game.GAME,
        check_data_func=check_data(second_player),
    )
    # data differ
    assert first_player_response[1] != second_player_response[1]
    # remove simulation
    first_player.question_pointer -= 1


@pytest.mark.parametrize(
    "answer_idx, expected_score, step",
    (
        # (0, 0, 1),
        (0, 0, 2),
        (1, 1, 3),
        (3, 2, 4),
        (3, 2, 5),
        # (4, 3, 6),
    ),
)
async def test__answer_next_question(
    clients: ClientsType, answer_idx, expected_score, step
):
    await u.emit_receive(
        clients,
        event=ClientEvent.ANSWER,
        data=u.get_valid_data(index=answer_idx),
        room=True,
        compare_responses=False,
    )
    answering_player, second_player = u.get_current_game(current_games).players
    assert answering_player.sid == clients[0].sid
    u.check_game_data(answering_player, expected_score, 0 + step)
    u.check_game_data(second_player, 0, 0)


async def test__answer_winner(clients: ClientsType):
    u.check_response(
        response=await u.emit_receive(
            clients,
            event=ClientEvent.ANSWER,
            data=u.get_valid_data(),
            room=True,
        ),
        expected_event=ServerEvent.Game.OVER,
        expected_data=Message.GAME_OVER.format(player="Alex"),
    )


@pytest.mark.skip(reason="Not in use")
async def test__disconnect(clients: ClientsType):
    *room, outside_user = clients
    assert outside_user.connected
    for c in room:
        assert not c.connected
