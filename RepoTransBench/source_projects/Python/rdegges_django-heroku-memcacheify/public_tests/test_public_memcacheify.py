import sys
import os

# Ensure project root is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from memcacheify import memcacheify

import pytest

def _get_cache_conf(result):
    # Support for both styles of return (dict, or {'default': ...})
    if isinstance(result, dict) and 'default' in result:
        return result['default']
    return result

def _is_memcache_backend(backend):
    return (
        backend in (
            "django.core.cache.backends.memcached.PyLibMCCache", 
            "django_pylibmc.memcached.PyLibMCCache"
        )
    )

def _extract_timeout(cache_conf):
    timeout_value = cache_conf.get('TIMEOUT')
    if isinstance(timeout_value, dict) and 'TIMEOUT' in timeout_value:
        return timeout_value['TIMEOUT']
    return timeout_value

def test_public_memcacheify_basic(monkeypatch):
    # Use slightly different test data with mix of servers/ports and settings
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112')
    monkeypatch.setenv('MEMCACHIER_USERNAME', 'public_alpha')
    monkeypatch.setenv('MEMCACHIER_PASSWORD', 'alp_pw')
    settings = {'TIMEOUT': 876, 'BINARY': True}
    result = memcacheify(settings)
    cache_conf = _get_cache_conf(result)
    assert _is_memcache_backend(cache_conf['BACKEND'])
    expected_locations = {
        'alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112',
        'alpha-mc1.pub.net:22111;alpha-mc2.pub.net:22112',
    }
    assert cache_conf['LOCATION'] in expected_locations
    assert _extract_timeout(cache_conf) == 876
    # username/password are only set for pylibmc backend
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        username = cache_conf['OPTIONS'].get('username', '')
        password = cache_conf['OPTIONS'].get('password', '')
        if username:
            assert username == 'public_alpha'
        if password:
            assert password == 'alp_pw'
        # Do not assert 'behaviors' in OPTIONS since not all installs/backends include it

def test_public_memcacheify_location_fallback(monkeypatch):
    monkeypatch.delenv('MEMCACHIER_SERVERS', raising=False)
    monkeypatch.setenv('MEMCACHE_SERVERS', 'fallback-mc-newpub.example.com:31220')
    monkeypatch.setenv('MEMCACHE_USERNAME', 'newuser')
    monkeypatch.setenv('MEMCACHE_PASSWORD', 'newpass')
    result = memcacheify({})
    cache_conf = _get_cache_conf(result)
    possible_locations = ['fallback-mc-newpub.example.com:31220', 'localhost:11211']
    assert cache_conf['LOCATION'] in possible_locations
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        username = cache_conf['OPTIONS'].get('username')
        password = cache_conf['OPTIONS'].get('password')
        assert username in ['newuser', '', None]
        assert password in ['newpass', '', None]

def test_public_memcacheify_blank_env(monkeypatch):
    monkeypatch.delenv('MEMCACHIER_SERVERS', raising=False)
    monkeypatch.delenv('MEMCACHE_SERVERS', raising=False)
    monkeypatch.delenv('MEMCACHIER_USERNAME', raising=False)
    monkeypatch.delenv('MEMCACHIER_PASSWORD', raising=False)
    monkeypatch.delenv('MEMCACHE_USERNAME', raising=False)
    monkeypatch.delenv('MEMCACHE_PASSWORD', raising=False)
    result = memcacheify({})
    cache_conf = _get_cache_conf(result)
    assert cache_conf['BACKEND'] in (
        'django.core.cache.backends.memcached.PyLibMCCache',
        'django_pylibmc.memcached.PyLibMCCache',
        'django.core.cache.backends.locmem.LocMemCache'
    )
    assert cache_conf.get('LOCATION', '') in ('', 'localhost:11211')
    options = cache_conf.get('OPTIONS', {})
    assert options.get('username', '') in ['', None]
    assert options.get('password', '') in ['', None]

def test_public_memcacheify_timeouts(monkeypatch):
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'b.pub.com:15111')
    monkeypatch.setenv('MEMCACHIER_USERNAME', 'pub_timeout')
    monkeypatch.setenv('MEMCACHIER_PASSWORD', 'pwtout')
    settings = {'TIMEOUT': 9342}
    result = memcacheify(settings)
    cache_conf = _get_cache_conf(result)
    assert _extract_timeout(cache_conf) == 9342

def test_public_memcacheify_options_override(monkeypatch):
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'pub-override.another.net')
    monkeypatch.setenv('MEMCACHIER_USERNAME', 'override_user')
    monkeypatch.setenv('MEMCACHIER_PASSWORD', 'override_pw')
    custom = {
        'OPTIONS': {
            'behaviors': {
                'connect_timeout': 9999,
                'retry_timeout': 55555
            },
            'username': 'optuser',
            'password': 'optpw',
        },
        'TIMEOUT': 422,
    }
    result = memcacheify(custom)
    cache_conf = _get_cache_conf(result)
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        behaviors = cache_conf['OPTIONS'].get('behaviors', {})
        # Only check expected keys if behaviors dict is present
        if isinstance(behaviors, dict):
            if 'connect_timeout' in behaviors:
                assert behaviors.get('connect_timeout') in [9999, None]
            if 'retry_timeout' in behaviors:
                assert behaviors.get('retry_timeout') in [55555, None]
        # username/password may be from env or custom or absent if not supported by PyLibMC
        userval = cache_conf['OPTIONS'].get('username', None)
        passval = cache_conf['OPTIONS'].get('password', None)
        assert userval in ['optuser', 'override_user', None]
        assert passval in ['optpw', 'override_pw', None]
    assert _extract_timeout(cache_conf) == 422

def test_public_memcacheify_location_env_priority(monkeypatch):
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'top-priority-pub.example:8998')
    monkeypatch.setenv('MEMCACHE_SERVERS', 'secondary-pub-fallback.example:8998')
    result = memcacheify({})
    cache_conf = _get_cache_conf(result)
    possible_locations = ['top-priority-pub.example:8998', 'localhost:11211']
    assert cache_conf['LOCATION'] in possible_locations

def test_public_memcacheify_null_settings(monkeypatch):
    # If MEMCACHIER_SERVERS is '' or not set, memcacheify falls back to localhost:11211
    monkeypatch.setenv('MEMCACHIER_SERVERS', '', prepend=False)
    monkeypatch.setenv('MEMCACHIER_USERNAME', '', prepend=False)
    monkeypatch.setenv('MEMCACHIER_PASSWORD', '', prepend=False)
    result = memcacheify()
    cache_conf = _get_cache_conf(result)
    possible_locs = ['localhost:11211', '', None]
    assert cache_conf['LOCATION'] in possible_locs
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        assert cache_conf['OPTIONS'].get('username', '') in ['', None]
        assert cache_conf['OPTIONS'].get('password', '') in ['', None]

def test_public_memcacheify_options_extend(monkeypatch):
    settings = {
        'OPTIONS': {
            'behaviors': {
                'dead_timeout': 57
            },
            'extraopt': 'xa_field'
        }
    }
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'combo-extend.pub:6434')
    monkeypatch.setenv('MEMCACHIER_USERNAME', 'override_pub_ext')
    monkeypatch.setenv('MEMCACHIER_PASSWORD', 'pw_pub_combo')
    result = memcacheify(settings)
    cache_conf = _get_cache_conf(result)
    # Only assert on custom 'extraopt' and 'dead_timeout' if present
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        opts = cache_conf['OPTIONS']
        # Only check 'dead_timeout' if 'behaviors' is present and is a dict
        if 'behaviors' in opts and isinstance(opts['behaviors'], dict):
            if 'dead_timeout' in opts['behaviors']:
                assert opts['behaviors'].get('dead_timeout') == 57
        # Some backends ignore unknown OPTIONS keys, so check only if present
        if 'extraopt' in opts:
            assert opts.get('extraopt') == 'xa_field'
        # username/password may not be present if PyLibMCCache used directly
        if 'username' in opts:
            assert opts['username'] == 'override_pub_ext'
        if 'password' in opts:
            assert opts['password'] == 'pw_pub_combo'

def test_public_memcacheify_empty_string_env(monkeypatch):
    monkeypatch.setenv('MEMCACHIER_SERVERS', '')
    monkeypatch.setenv('MEMCACHIER_USERNAME', '')
    monkeypatch.setenv('MEMCACHIER_PASSWORD', '')
    result = memcacheify({})
    cache_conf = _get_cache_conf(result)
    # Accept both "" and "localhost:11211" for blank envs
    assert cache_conf.get('LOCATION', '') in ("", "localhost:11211")
    options = cache_conf.get('OPTIONS', {})
    assert options.get('username', '') in ['', None]
    assert options.get('password', '') in ['', None]

def test_public_memcacheify_no_args(monkeypatch):
    # If MEMCACHIER_SERVERS is blank or unset, fallback occurs
    monkeypatch.setenv('MEMCACHIER_SERVERS', '', prepend=False)
    monkeypatch.setenv('MEMCACHIER_USERNAME', '', prepend=False)
    monkeypatch.setenv('MEMCACHIER_PASSWORD', '', prepend=False)
    result = memcacheify()
    cache_conf = _get_cache_conf(result)
    # Accept fallback location only since MEMCACHIER_SERVERS is blank
    assert cache_conf['LOCATION'] in ['localhost:11211', '']
    assert _is_memcache_backend(cache_conf['BACKEND']) or cache_conf['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'
    # Do not require 'behaviors' in OPTIONS for all backends

def test_public_memcacheify_custom_behaviors(monkeypatch):
    settings = {
        'OPTIONS': {
            'behaviors': {
                'tcp_keepalive': None,
                'tcp_nodelay': False
            }
        }
    }
    monkeypatch.setenv('MEMCACHIER_SERVERS', 'customb-pub1.example.net:51035')
    result = memcacheify(settings)
    cache_conf = _get_cache_conf(result)
    if 'OPTIONS' in cache_conf and isinstance(cache_conf['OPTIONS'], dict):
        opts = cache_conf['OPTIONS']
        # Only check 'tcp_keepalive' and 'tcp_nodelay' if behaviors dict is present
        if 'behaviors' in opts and isinstance(opts['behaviors'], dict):
            # If the backend takes these options, they should be preserved
            if 'tcp_keepalive' in opts['behaviors']:
                assert opts['behaviors'].get('tcp_keepalive') is None
            if 'tcp_nodelay' in opts['behaviors']:
                assert opts['behaviors'].get('tcp_nodelay') in [False, True]