import pytest
import pytest_asyncio
import threading as th
import uvicorn

from ..main import app
from .types import ClientType, ClientsType


class AppTest:
    base_url: str = 'http://127.0.0.1:8000'
    clients_amount = 3
    scope = 'module'
    timeout = 0.1

    @staticmethod
    def run_app(app):
        th.Thread(target=lambda: uvicorn.run(app), daemon=True).start()

    @staticmethod
    def single_loop(scope: str = 'module'):
        return pytest.mark.asyncio(loop_scope=scope)


single_loop_module = AppTest.single_loop()
pytestmark = single_loop_module
AppTest.run_app(app)


async def connect_client() -> ClientType:
    client = ClientType()
    await client.connect(AppTest.base_url)
    return client


@pytest_asyncio.fixture(scope=AppTest.scope)
async def clients() -> ClientsType:
    return [await connect_client() for _ in range(AppTest.clients_amount)]


'''@pytest_asyncio.fixture(scope=SCOPE)
async def sio() -> AsyncSimpleClient:
    return await connect_client()


@pytest_asyncio.fixture(scope=SCOPE)
async def sio2() -> AsyncSimpleClient:
    return await connect_client()'''

'''@pytest.fixture(scope=SCOPE)
def clients(sio, sio2) -> tuple[AsyncSimpleClient]:
    assert sio.sid != sio2.sid
    return sio, sio2'''

'''
from typing import AsyncGenerator
@pytest_asyncio.fixture  # (scope='module')
async def sio(url: str = TEST_URL) -> AsyncGenerator[AsyncSimpleClient, None]:
    async with AsyncSimpleClient() as client:
        await client.connect(url)
        yield client
'''


'''
@pytest.fixture
def client():
    sio = Client()
    yield sio
    sio.disconnect()


@pytest.fixture
def events(client):
    """ Фикстура для отлова всех эвентов которые приходят от бэка клиенту """
    all_events = {}

    def event_handler(event, data):
        all_events[event] = data

    client.on('*', event_handler)
    yield all_events
'''
