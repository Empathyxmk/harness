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
        # Dummy implementation: only BTCUSDT supported
        if symbol != "BTCUSDT":
            return -1
        return 1

    def sell(self, symbol, amount):
        if not self._connected:
            return -1
        if not symbol or amount is None or amount <= 0:
            return -1
        # Dummy implementation: only BTCUSDT supported
        if symbol != "BTCUSDT":
            return -1
        return 1

def test_connection_logic():
    client = TradingClient()
    assert not client.is_connected()
    client.connect()
    assert client.is_connected()
    client.disconnect()
    assert not client.is_connected()

def test_buy_sell_success():
    client = TradingClient()
    client.connect()
    assert client.buy("BTCUSDT", 0.002) == 1
    assert client.sell("BTCUSDT", 0.002) == 1

def test_buy_sell_fail_when_not_connected():
    client = TradingClient()
    assert client.buy("BTCUSDT", 0.002) == -1
    assert client.sell("BTCUSDT", 0.002) == -1

def test_buy_sell_invalid_input():
    client = TradingClient()
    client.connect()
    assert client.buy(None, 0.002) == -1
    assert client.buy("BTCUSDT", 0) == -1
    assert client.sell(None, 0.002) == -1
    assert client.sell("BTCUSDT", -42) == -1