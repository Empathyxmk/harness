import pytest
from pyope import errors

def test_invalid_ciphertext_error():
    with pytest.raises(errors.InvalidCiphertextError):
        raise errors.InvalidCiphertextError("Cipher error")

def test_invalid_range_limits_error():
    with pytest.raises(errors.InvalidRangeLimitsError):
        raise errors.InvalidRangeLimitsError("Range error")

def test_out_of_range_error():
    with pytest.raises(errors.OutOfRangeError):
        raise errors.OutOfRangeError("Out of range")

def test_not_enough_coins_error():
    with pytest.raises(errors.NotEnoughCoinsError):
        raise errors.NotEnoughCoinsError("No coins left")

def test_invalid_coin_error():
    with pytest.raises(errors.InvalidCoinError):
        raise errors.InvalidCoinError("Invalid coin")