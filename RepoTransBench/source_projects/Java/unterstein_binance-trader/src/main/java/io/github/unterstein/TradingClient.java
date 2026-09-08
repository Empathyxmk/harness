package io.github.unterstein;

// Stubbed TradingClient for test/coverage purpose, removes Binance dependency

public class TradingClient {

    private boolean connected;

    public TradingClient() {
        connected = false;
    }

    public void connect() {
        connected = true;
    }

    public void disconnect() {
        connected = false;
    }

    public boolean isConnected() {
        return connected;
    }

    public int buy(String symbol, double quantity) {
        if (!connected || symbol == null || quantity <= 0) {
            return -1;
        }
        return 1;
    }

    public int sell(String symbol, double quantity) {
        if (!connected || symbol == null || quantity <= 0) {
            return -1;
        }
        return 1;
    }
}