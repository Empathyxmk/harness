package io.github.unterstein;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TradingClientPublicTest {

    TradingClient client;

    @BeforeEach
    void setUp() {
        client = new TradingClient();
    }

    @Test
    void testBuyWithDifferentSymbolPublic() {
        // Use a symbol that is NOT supported by dummy impl; expect failure!
        int result = client.buy("XRPUSDT", 150);
        assertEquals(-1, result, "Expected failure for unsupported symbol buy in TradingClient public test");
    }

    @Test
    void testSellWithDifferentSymbolPublic() {
        // Use a symbol that is NOT supported by dummy impl; expect failure!
        int result = client.sell("LTCUSDT", 200);
        assertEquals(-1, result, "Expected failure for unsupported symbol sell in TradingClient public test");
    }

    @Test
    void testBuySellInvalidAmountPublic() {
        // Use a different invalid negative amount
        int resultBuy = client.buy("BTCUSDT", -77);
        assertEquals(-1, resultBuy, "Expected failure for negative amount (public test)");

        int resultSell = client.sell("ETHUSDT", -33);
        assertEquals(-1, resultSell, "Expected failure for negative sell amount (public test)");
    }

    @Test
    void testBuySellInvalidInputPublic() {
        // Use null and empty string, should still fail
        int resultBuyNull = client.buy(null, 10);
        assertEquals(-1, resultBuyNull, "Expected failure for null symbol buy");

        int resultBuyEmpty = client.buy("", 10);
        assertEquals(-1, resultBuyEmpty, "Expected failure for empty symbol buy");

        int resultSellNull = client.sell(null, 5);
        assertEquals(-1, resultSellNull, "Expected failure for null symbol sell");

        int resultSellEmpty = client.sell("", 5);
        assertEquals(-1, resultSellEmpty, "Expected failure for empty symbol sell");
    }
}