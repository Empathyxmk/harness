import adblockparser

def test_public_imports_available():
    assert hasattr(adblockparser, 'AdblockRules')
    assert hasattr(adblockparser, 'AdblockRule')
    assert hasattr(adblockparser, 'AdblockParsingError')