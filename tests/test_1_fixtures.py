from .conftest import AppTest
from .types import ClientType, ClientsType


def test__clients_fixture(clients: ClientsType):
    assert len(clients) == AppTest.clients_amount
    unique_sids = set()
    for c in clients:
        assert isinstance(c, ClientType)
        assert c.connected
        unique_sids.add(c.sid)

    assert len(unique_sids) == AppTest.clients_amount
