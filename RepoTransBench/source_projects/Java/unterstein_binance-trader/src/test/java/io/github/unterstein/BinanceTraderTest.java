package io.github.unterstein;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BinanceTraderTest {

    @Test
    void testTradeSuccess() {
        TradingClient client = new TradingClient();
        BinanceTrader trader = new BinanceTrader(client);
        boolean result = trader.trade("BTCUSDT", 1.0, 2.0);
        assertTrue(result);
        trader.shutdown();
        assertFalse(client.isConnected());
    }

    @Test
    void testTradeFailureDueToInput() {
        TradingClient client = new TradingClient();
        BinanceTrader trader = new BinanceTrader(client);
        // Should fail buy due to invalid quantity
        boolean result = trader.trade("BTCUSDT", 0.0, 2.0);
        assertFalse(result);
        trader.shutdown();
    }
}