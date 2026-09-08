package io.github.unterstein;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TradingClientTest {

    @Test
    void testConnectionLogic() {
        TradingClient client = new TradingClient();
        assertFalse(client.isConnected());
        client.connect();
        assertTrue(client.isConnected());
        client.disconnect();
        assertFalse(client.isConnected());
    }

    @Test
    void testBuySellSuccess() {
        TradingClient client = new TradingClient();
        client.connect();
        assertEquals(1, client.buy("BTCUSDT", 0.002));
        assertEquals(1, client.sell("BTCUSDT", 0.002));
    }

    @Test
    void testBuySellFailWhenNotConnected() {
        TradingClient client = new TradingClient();
        assertEquals(-1, client.buy("BTCUSDT", 0.002));
        assertEquals(-1, client.sell("BTCUSDT", 0.002));
    }

    @Test
    void testBuySellInvalidInput() {
        TradingClient client = new TradingClient();
        client.connect();
        assertEquals(-1, client.buy(null, 0.002));
        assertEquals(-1, client.buy("BTCUSDT", 0));
        assertEquals(-1, client.sell(null, 0.002));
        assertEquals(-1, client.sell("BTCUSDT", -42));
    }
}