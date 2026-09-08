package io.github.unterstein;

// Stubbed BinanceBotApplication for test/coverage purpose

public class BinanceBotApplication {

    public static void main(String[] args) {
        TradingClient client = new TradingClient();
        BinanceTrader trader = new BinanceTrader(client);
        trader.trade("BTCUSDT", 0.001, 0.001);
        trader.shutdown();
    }
}