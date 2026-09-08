package io.github.unterstein;

// Stubbed BinanceTrader for test/coverage purpose

public class BinanceTrader {

    private TradingClient client;

    public BinanceTrader(TradingClient client) {
        this.client = client;
    }

    public boolean trade(String symbol, double buyQty, double sellQty) {
        if (!client.isConnected()) {
            client.connect();
        }
        int buyResult = client.buy(symbol, buyQty);
        int sellResult = client.sell(symbol, sellQty);
        return buyResult == 1 && sellResult == 1;
    }

    public void shutdown() {
        client.disconnect();
    }
}