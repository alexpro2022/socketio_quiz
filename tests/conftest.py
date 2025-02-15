import threading as th

import pytest
import pytest_asyncio
import uvicorn

from src.web.app import app

from .types import ClientsType, ClientType


class AppTest:
    LOCALHOSTS = ("0.0.0.0", "127.0.0.1")
    host: str = LOCALHOSTS[0]
    port: int = 8000
    base_url: str = f"http://{'localhost' if host in LOCALHOSTS else host}:{port}"
    clients_amount = 3
    scope = "module"
    timeout = 0.1

    @classmethod
    def run_app(cls, app):
        th.Thread(
            target=lambda: uvicorn.run(app, host=cls.host, port=cls.port), daemon=True
        ).start()

    @staticmethod
    def single_loop(scope: str = "module"):
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
