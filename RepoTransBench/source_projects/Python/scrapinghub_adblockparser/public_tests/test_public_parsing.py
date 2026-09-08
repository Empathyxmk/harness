import pytest
from adblockparser import AdblockRules

rules = [
    '/track.js$script',
    '/log.gif$image',
    '||adnetwork.com^$third-party',
    '@@||safe.com/banner.gif$image',
]

adp = AdblockRules(rules)

def test_public_block_script():
    assert adp.should_block('http://another.com/track.js', {'script': True}) is True
    assert adp.should_block('http://another.com/track.js', {'image': True}) is False

def test_public_block_image():
    assert adp.should_block('http://foo.com/track.gif', {'image': True}) is False
    assert adp.should_block('http://foo.com/log.gif', {'image': True}) is True

def test_public_third_party():
    assert adp.should_block('http://x.yz/ad.js', {'third-party': True}) is False
    assert adp.should_block('http://adnetwork.com/adv_banner.jpg', {'third-party': True}) is True

def test_public_exception():
    assert adp.should_block('http://safe.com/banner.gif', {'image': True}) is False