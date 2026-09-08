import pytest

# --- Mock classes as stubs for translation ---

class MockConnection:
    # Simulate simple key-value storage
    def __init__(self):
        self.storage = {}

    async def start(self):
        pass

    async def stop(self):
        pass

    async def get(self, key):
        key_tuple = (key['id'], key['segment'])
        if key_tuple in self.storage:
            return {'item': self.storage[key_tuple]}
        return None

    async def set(self, key, value, ttl):
        key_tuple = (key['id'], key['segment'])
        self.storage[key_tuple] = value

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

    async def set(self, key, value, ttl):
        await self.connection.set(key, value, ttl)

    async def get(self, key):
        return await self.connection.get(key)

# ---- Tests ----

import asyncio

@pytest.mark.asyncio
class TestClientPublic:
    async def test_uses_prototype_engine_with_new_key_item(self):
        client = CatboxClient(MockConnection)
        await client.start()

        key = {'id': 'y', 'segment': 'demo'}
        await client.set(key, 'ABC', 1500)

        result = await client.get(key)
        assert result['item'] == 'ABC'

    async def test_supports_empty_keys_different_segment(self):
        client = CatboxClient(MockConnection)
        await client.start()

        key = {'id': '', 'segment': 'public_segment'}
        await client.set(key, 'XYZ', 2000)

        result = await client.get(key)
        assert result['item'] == 'XYZ'