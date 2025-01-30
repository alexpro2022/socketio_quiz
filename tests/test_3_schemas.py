from uuid import uuid4
import pytest
# from pydantic import ValidationError
from src.pydantic.schemas import Topic, Question, JoinGame, Player, Answer, Game, GameOut
from src.repository.db.data import QUESTIONS
from src.repository.db.crud import fetch_all
from .conftest import single_loop_module  # noqa


@pytest.mark.parametrize('model, data, expected', (
    (Topic, dict(pk=0, name='name'), None),
    (JoinGame, dict(topic_pk=0, name='name'), None),
    (Question, dict(pk=0, topic=0, text='text', options=['a', 's', 'd'], answer=0), None),
    (Player, dict(sid='sid', name='name'), dict(sid='sid', name='name', score=0, current_question=0, question_count=0)),
    (Answer, dict(index=0, game_uid=uuid4()), None),
))
def test__valid_data(model, data, expected):
    instance = model(**data)
    assert instance.model_dump() == expected or data


@pytest.mark.parametrize('model, data', (
    (Topic, dict(pk=-1, name='name')),
    (Topic, dict(pk=0, name='')),
    (Topic, dict(pk=0, name=1)),
    #
    (JoinGame, dict(topic_pk=-1, name='name')),
    (JoinGame, dict(topic_pk=0, name='')),
    (JoinGame, dict(topic_pk=0, name=1)),
    #
    (Question, dict(pk=-1, topic=0, text='text', options=['a', 's', 'd'], answer=0)),
    (Question, dict(pk=0, topic=-1, text='text', options=['a', 's', 'd'], answer=0)),
    (Question, dict(pk=0, topic=0, text='', options=['a', 's', 'd'], answer=0)),
    (Question, dict(pk=0, topic=0, text=1, options=['a', 's', 'd'], answer=0)),
    (Question, dict(pk=0, topic=0, text='text', options=['', 's', 'd'], answer=0)),
    (Question, dict(pk=0, topic=0, text='text', options=[1, 2, 3], answer=0)),
    (Question, dict(pk=0, topic=0, text='text', options=['a', 's', 'd'], answer=-1)),
    #
    (Player, dict(sid='', name='name')),
    (Player, dict(sid='sid', name='')),
    #
    (Answer, dict(index=-1, game_uid=uuid4())),
    (Answer, dict(index=0, game_uid=1)),
))
def test__invalid_pk(model, data):
    with pytest.raises(ValueError):  # ValueError == pydantic.ValidationError
        model(**data)


@single_loop_module
async def test__Game_init():
    game = Game(
        uid=uuid4(),
        questions=await fetch_all(QUESTIONS, topic=5),
        players=[Player(sid='sid1', name='name1'), Player(sid='sid2', name='name2')]
    )
    game_data = game.init()
    GameOut.model_validate(game_data)
    # GameOut.model_validate_json(game_data)
