import pytest

class TradingClient:
    def __init__(self):
        self._connected = False

    def is_connected(self):
        return self._connected

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def buy(self, symbol, amount):
        if not self._connected:
            return -1
        if not symbol or amount is None or amount <= 0:
            return -1
        # Only BTCUSDT supported in dummy
        if symbol != "BTCUSDT":
            return -1
        return 1

    def sell(self, symbol, amount):
        if not self._connected:
            return -1
        if not symbol or amount is None or amount <= 0:
            return -1
        # Only BTCUSDT supported in dummy
        if symbol != "BTCUSDT":
            return -1
        return 1

import pytest

@pytest.fixture(autouse=True)
def client():
    c = TradingClient()
    yield c

def test_buy_with_different_symbol_public(client):
    # Use a symbol NOT supported by dummy impl; expect failure!
    result = client.buy("XRPUSDT", 150)
    assert result == -1, "Expected failure for unsupported symbol buy in TradingClient public test"

def test_sell_with_different_symbol_public(client):
    # Use a symbol NOT supported by dummy impl; expect failure!
    result = client.sell("LTCUSDT", 200)
    assert result == -1, "Expected failure for unsupported symbol sell in TradingClient public test"

def test_buy_sell_invalid_amount_public(client):
    result_buy = client.buy("BTCUSDT", -77)
    assert result_buy == -1, "Expected failure for negative amount (public test)"

    result_sell = client.sell("ETHUSDT", -33)
    assert result_sell == -1, "Expected failure for negative sell amount (public test)"

def test_buy_sell_invalid_input_public(client):
    result_buy_null = client.buy(None, 10)
    assert result_buy_null == -1, "Expected failure for null symbol buy"

    result_buy_empty = client.buy("", 10)
    assert result_buy_empty == -1, "Expected failure for empty symbol buy"

    result_sell_null = client.sell(None, 5)
    assert result_sell_null == -1, "Expected failure for null symbol sell"

    result_sell_empty = client.sell("", 5)
    assert result_sell_empty == -1, "Expected failure for empty symbol sell"