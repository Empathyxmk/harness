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

class BinanceTrader:
    def __init__(self, client):
        self.client = client
        self.client.connect()

    def trade(self, symbol, buy_qty, sell_qty):
        if buy_qty is None or buy_qty <= 0 or not symbol:
            return False
        buy_res = self.client.buy(symbol, buy_qty)
        if buy_res == 1:
            sell_res = self.client.sell(symbol, sell_qty)
            return sell_res == 1
        return False

    def shutdown(self):
        self.client.disconnect()

def test_trade_success():
    client = TradingClient()
    trader = BinanceTrader(client)
    result = trader.trade("BTCUSDT", 1.0, 2.0)
    assert result
    trader.shutdown()
    assert not client.is_connected()

def test_trade_failure_due_to_input():
    client = TradingClient()
    trader = BinanceTrader(client)
    result = trader.trade("BTCUSDT", 0.0, 2.0)
    assert not result
    trader.shutdown()