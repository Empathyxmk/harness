package io.github.unterstein;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BinanceTraderPublicTest {

    @Test
    void testTradeSuccessPublic() {
        TradingClient client = new TradingClient();
        BinanceTrader trader = new BinanceTrader(client);
        boolean result = trader.trade("ETHUSDT", 3.0, 1.0);  // Different symbol, different quantities
        assertTrue(result);
        trader.shutdown();
        assertFalse(client.isConnected());
    }

    @Test
    void testTradeFailureDueToInputPublic() {
        TradingClient client = new TradingClient();
        BinanceTrader trader = new BinanceTrader(client);
        // Should fail buy due to null symbol
        boolean result = trader.trade(null, 2.0, 1.5);
        assertFalse(result);
        trader.shutdown();
    }
}