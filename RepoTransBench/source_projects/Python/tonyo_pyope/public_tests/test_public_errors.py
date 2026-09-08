import pytest
from pyope.errors import NotEnoughCoinsError, InvalidCoinError

def test_not_enough_coins_error_public():
    with pytest.raises(NotEnoughCoinsError) as exc_info:
        raise NotEnoughCoinsError("Public not enough coins")
    assert "Public not enough coins" in str(exc_info.value)

def test_invalid_coin_error_public():
    with pytest.raises(InvalidCoinError) as exc_info:
        raise InvalidCoinError("Public invalid coin")
    assert "Public invalid coin" in str(exc_info.value)

def test_not_enough_coins_error_type_public():
    exc = NotEnoughCoinsError("foo")
    assert isinstance(exc, Exception)

def test_invalid_coin_error_type_public():
    exc = InvalidCoinError("bar")
    assert isinstance(exc, Exception)

def test_error_messages_public():
    assert str(NotEnoughCoinsError("msg1")) == "msg1"
    assert str(InvalidCoinError("msg2")) == "msg2"