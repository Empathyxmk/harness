import pytest

# --- Mock classes ---

class MockConnection:
    def __init__(self):
        self.storage = {}
    async def start(self):
        pass
    async def stop(self):
        pass
    async def set(self, key, value, ttl):
        self.storage[key] = value
    async def get(self, key):
        return {'item': self.storage.get(key, None)}

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

    @property
    def is_ready(self):
        return self._ready

class CatboxPolicy:
    def __init__(self, policy_opts, client, segment):
        self.opts = policy_opts
        self.client = client
        self.segment = segment
        self._stats = {'sets': 0, 'gets': 0, 'hits': 0, 'stales': 0, 'generates': 0, 'errors': 0}
        self._store = {}

    @property
    def stats(self):
        return self._stats

    async def set(self, key, value, ttl):
        self._store[key] = value
        self._stats['sets'] += 1

    async def get(self, key):
        self._stats['gets'] += 1
        if key in self._store:
            self._stats['hits'] += 1
            return self._store[key]
        else:
            return None

@pytest.mark.asyncio
class TestPolicyPublic:
    async def test_returns_cached_item_with_different_value(self):
        client = CatboxClient(MockConnection)
        policy = CatboxPolicy({'expiresIn': 1200}, client, 'public')

        # Test .client shallow equality
        assert policy.client is client

        await client.start()
        await policy.set('myKey', 'publicItem', None)
        value = await policy.get('myKey')

        assert value == 'publicItem'
        assert policy.stats == {'sets': 1, 'gets': 1, 'hits': 1, 'stales': 0, 'generates': 0, 'errors': 0}

    async def test_works_with_special_property_names_different_key_names(self):
        client = CatboxClient(MockConnection)
        policy = CatboxPolicy({'expiresIn': 900}, client, 'public_test')
        await client.start()

        await policy.set('__proto__', 'foo', None)
        await policy.set('constructor', 'bar', None)

        v1 = await policy.get('__proto__')
        v2 = await policy.get('constructor')

        assert v1 == 'foo'
        assert v2 == 'bar'