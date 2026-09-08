import pytest
from adblockparser import AdblockRule

def test_public_parse_options_simple():
    r = AdblockRule('/ad.js$script,domain=example.com|another.net')
    assert 'script' in r.options
    assert 'domain' in r.options
    assert r.options['domain'] == {'example.com', 'another.net'}

def test_public_parse_options_no_options():
    r = AdblockRule('/track.gif')
    assert r.options == {}

def test_public_parse_options_complex():
    r = AdblockRule('/analytics.js$image,third-party,domain=mysite.org|anothersite.co.uk')
    assert 'image' in r.options
    assert 'third-party' in r.options
    assert r.options['domain'] == {'mysite.org', 'anothersite.co.uk'}

def test_public_parse_options_exception():
    r = AdblockRule('@@/nocache.png$subdocument,domain=sub.example.org')
    assert r.is_exception
    assert 'subdocument' in r.options
    assert r.options['domain'] == {'sub.example.org'}