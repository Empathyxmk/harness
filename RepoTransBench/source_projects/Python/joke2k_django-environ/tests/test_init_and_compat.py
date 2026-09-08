import types
import sys
import importlib
import builtins

import environ.__init__ as ei
import environ.compat as ec


def test_environ_meta_variables():
    # Test meta information exports in __init__.py
    assert isinstance(ei.__copyright__, str)
    assert isinstance(ei.__version__, str)
    assert isinstance(ei.__license__, str)
    assert isinstance(ei.__author__, str)
    assert isinstance(ei.__author_email__, str)
    assert isinstance(ei.__maintainer__, str)
    assert isinstance(ei.__maintainer_email__, str)
    assert isinstance(ei.__url__, str)
    assert isinstance(ei.__description__, str)


def test_choose_rediscache_driver_precedence(monkeypatch):
    # Patch find_spec to simulate django_redis present/django absent
    monkeypatch.setattr(ec, "find_spec", lambda n: n == "django_redis")
    val = ec.choose_rediscache_driver()
    assert val == "django_redis.cache.RedisCache"


def test_choose_rediscache_driver_builtin(monkeypatch):
    # Patch find_spec and DJANGO_VERSION to simulate django present (>=4.0)
    monkeypatch.setattr(ec, "find_spec", lambda n: False)
    monkeypatch.setattr(ec, "DJANGO_VERSION", (4, 0))
    val = ec.choose_rediscache_driver()
    assert val == "django.core.cache.backends.redis.RedisCache"
    # Reset value for global state
    monkeypatch.setattr(ec, "DJANGO_VERSION", None, raising=False)


def test_choose_rediscache_driver_redis_cache(monkeypatch):
    # Patch find_spec and DJANGO_VERSION to simulate django < 4 and no django_redis
    monkeypatch.setattr(ec, "find_spec", lambda n: False)
    monkeypatch.setattr(ec, "DJANGO_VERSION", (3, 2))
    val = ec.choose_rediscache_driver()
    assert val == "redis_cache.RedisCache"
    # Reset value for global state
    monkeypatch.setattr(ec, "DJANGO_VERSION", None, raising=False)


def test_choose_postgres_driver(monkeypatch):
    monkeypatch.setattr(ec, "DJANGO_VERSION", (1, 11))
    assert ec.choose_postgres_driver() == "django.db.backends.postgresql_psycopg2"
    monkeypatch.setattr(ec, "DJANGO_VERSION", (3, 2))
    assert ec.choose_postgres_driver() == "django.db.backends.postgresql"
    monkeypatch.setattr(ec, "DJANGO_VERSION", None)
    assert ec.choose_postgres_driver() == "django.db.backends.postgresql"


def test_choose_pymemcache_driver(monkeypatch):
    monkeypatch.setattr(ec, "DJANGO_VERSION", (1, 11))
    assert ec.choose_pymemcache_driver() == "django.core.cache.backends.memcached.PyLibMCCache"
    monkeypatch.setattr(ec, "DJANGO_VERSION", (3, 2))
    monkeypatch.setattr(ec, "find_spec", lambda n: False)
    assert ec.choose_pymemcache_driver() == "django.core.cache.backends.memcached.PyLibMCCache"
    monkeypatch.setattr(ec, "find_spec", lambda n: True)
    assert ec.choose_pymemcache_driver() == "django.core.cache.backends.memcached.PyMemcacheCache"
    monkeypatch.setattr(ec, "DJANGO_VERSION", None)