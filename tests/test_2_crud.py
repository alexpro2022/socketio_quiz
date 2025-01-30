import pytest
from src.repository.db import crud as c
from src.repository.db import data as d
from .conftest import pytestmark  # noqa


TOPIC = 6
EXPECTED = [d.Question(pk=1, topic=TOPIC, text='Кто является первым автором языка программирования C++?', options=['Линус Торвальдс', 'Бьёрн Страуструп', 'Джеймс Гослинг', 'Кен Томпсон'], answer=2)]
parametrize = pytest.mark.parametrize('kwargs, expected', (
    ({}, d.QUESTIONS),
    (dict(pk=1, topic=TOPIC), EXPECTED),
    (dict(asd=1), []),  # None for fetch_one
))


@parametrize
async def test__fetch_all(kwargs, expected):
    res = await c.fetch_all(d.QUESTIONS, **kwargs)
    assert res == expected


@parametrize
async def test__fetch_one(kwargs, expected):
    res = await c.fetch_one(d.QUESTIONS, **kwargs)
    assert res == (expected[0] if expected else None)
