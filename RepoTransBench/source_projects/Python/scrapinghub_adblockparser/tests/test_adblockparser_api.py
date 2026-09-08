import adblockparser

def test_imports_available():
    assert hasattr(adblockparser, 'AdblockRules')
    assert hasattr(adblockparser, 'AdblockRule')
    assert hasattr(adblockparser, 'AdblockParsingError')