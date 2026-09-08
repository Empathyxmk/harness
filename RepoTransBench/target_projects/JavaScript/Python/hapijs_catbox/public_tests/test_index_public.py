import pytest

# --- Mock classes ---

class MockConnection:
    def __init__(self):
        self.storage = {}
    async def start(self):
        pass
    async def stop(self):
        pass

class CatboxClient:
    def __init__(self, connection_factory):
        self.connection = connection_factory()
        self._ready = False

    async def start(self):
        await self.connection.start()
        self._ready = True

    async def stop(self):
        await self.connection.stop()
        self._ready = False

    def isReady(self):
        return self._ready

@pytest.mark.asyncio
class TestCatboxPublic:
    async def test_creates_a_new_connection_public(self):
        client = CatboxClient(MockConnection)
        await client.start()
        assert client.isReady() is True

    async def test_closes_the_connection_public(self):
        client = CatboxClient(MockConnection)
        await client.start()
        assert client.isReady() is True
        await client.stop()
        assert client.isReady() is False