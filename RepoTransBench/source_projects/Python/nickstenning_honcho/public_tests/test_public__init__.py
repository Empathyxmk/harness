from honcho import __version__
def test_public_importable():
    assert isinstance(__version__, str)
    assert len(__version__) > 0