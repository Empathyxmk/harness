import os
import pytest
from memcacheify import memcacheify

@pytest.fixture(autouse=True)
def clean_environ(monkeypatch):
    relevant = [
        'MEMCACHE_PASSWORD', 'MEMCACHE_SERVERS', 'MEMCACHE_USERNAME',
        'MEMCACHIER_PASSWORD', 'MEMCACHIER_SERVERS', 'MEMCACHIER_USERNAME',
        'MEMCACHEDCLOUD_PASSWORD', 'MEMCACHEDCLOUD_SERVERS', 'MEMCACHEDCLOUD_USERNAME',
        'MEMCACHEIFY_USE_LOCAL'
    ]
    originals = {k: os.environ[k] for k in relevant if k in os.environ}
    for k in relevant:
        os.environ.pop(k, None)
    yield
    for k in relevant:
        os.environ.pop(k, None)
    os.environ.update(originals)

def test_local_cache_default():
    caches = memcacheify()
    assert caches['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'

def test_memcache_env_vars_missing(monkeypatch):
    os.environ['MEMCACHE_PASSWORD'] = 'pass'
    os.environ['MEMCACHE_SERVERS'] = 'host'
    # username missing
    caches = memcacheify()
    assert caches['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'

def test_memcache_env_vars_set(monkeypatch):
    os.environ['MEMCACHE_PASSWORD'] = 'pass'
    os.environ['MEMCACHE_SERVERS'] = 'host'
    os.environ['MEMCACHE_USERNAME'] = 'user'
    caches = memcacheify(timeout=111)
    assert caches['default']['BACKEND'] == 'django_pylibmc.memcached.PyLibMCCache'
    assert caches['default']['LOCATION'] == 'localhost:11211'
    assert caches['default']['TIMEOUT'] == 111

def test_memcachier_env_vars_set(monkeypatch):
    os.environ['MEMCACHIER_PASSWORD'] = 'pw'
    os.environ['MEMCACHIER_SERVERS'] = 'host1,host2'
    os.environ['MEMCACHIER_USERNAME'] = 'user'
    caches = memcacheify(timeout=123)
    assert caches['default']['LOCATION'] == 'host1;host2'
    assert caches['default']['TIMEOUT'] == 123
    assert os.environ['MEMCACHE_SERVERS'] == 'host1;host2'
    assert os.environ['MEMCACHE_USERNAME'] == 'user'
    assert os.environ['MEMCACHE_PASSWORD'] == 'pw'
    assert caches['default']['BACKEND'] == 'django_pylibmc.memcached.PyLibMCCache'

def test_memcachedcloud_env_vars_set(monkeypatch):
    os.environ['MEMCACHEDCLOUD_PASSWORD'] = 'pwcloud'
    os.environ['MEMCACHEDCLOUD_SERVERS'] = 'c1,c2'
    os.environ['MEMCACHEDCLOUD_USERNAME'] = 'clouduser'
    caches = memcacheify(timeout=321)
    assert caches['default']['LOCATION'] == 'c1;c2'
    assert caches['default']['TIMEOUT'] == 321
    assert os.environ['MEMCACHE_SERVERS'] == 'c1;c2'
    assert os.environ['MEMCACHE_USERNAME'] == 'clouduser'
    assert os.environ['MEMCACHE_PASSWORD'] == 'pwcloud'
    assert caches['default']['BACKEND'] == 'django_pylibmc.memcached.PyLibMCCache'

def test_memcacheify_use_local(monkeypatch):
    os.environ['MEMCACHEIFY_USE_LOCAL'] = '1'
    caches = memcacheify()
    assert caches['default']['BACKEND'] == 'django_pylibmc.memcached.PyLibMCCache'

@pytest.mark.parametrize("missing_envs", [
    ["MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS"], # missing two
    ["MEMCACHIER_PASSWORD"],                       # missing one
])
def test_memcachier_incomplete(missing_envs):
    os.environ['MEMCACHIER_PASSWORD'] = 'pw'
    os.environ['MEMCACHIER_SERVERS'] = 'h1'
    os.environ['MEMCACHIER_USERNAME'] = 'u1'
    for m in missing_envs:
        os.environ.pop(m, None)
    caches = memcacheify()
    assert caches['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'

@pytest.mark.parametrize("missing_envs", [
    ["MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS"],
    ["MEMCACHEDCLOUD_PASSWORD"],
])
def test_memcachedcloud_incomplete(missing_envs):
    os.environ['MEMCACHEDCLOUD_PASSWORD'] = 'pw'
    os.environ['MEMCACHEDCLOUD_SERVERS'] = 'h1'
    os.environ['MEMCACHEDCLOUD_USERNAME'] = 'u1'
    for m in missing_envs:
        os.environ.pop(m, None)
    caches = memcacheify()
    assert caches['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'

def test_memcacheify_timeout_default():
    os.environ['MEMCACHE_PASSWORD'] = 'p'
    os.environ['MEMCACHE_SERVERS'] = 'h'
    os.environ['MEMCACHE_USERNAME'] = 'u'
    caches = memcacheify()
    # Should default to 500
    assert caches['default']['TIMEOUT'] == 500