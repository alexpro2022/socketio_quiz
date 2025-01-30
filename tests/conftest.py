import pytest
import pytest_asyncio
import threading as th
import uvicorn

from src.web.app import app
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
