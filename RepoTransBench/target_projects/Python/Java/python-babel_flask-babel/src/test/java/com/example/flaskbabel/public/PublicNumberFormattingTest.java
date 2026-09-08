package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;

class PublicNumberFormattingTest {

    @Test
    void testPublicFormatNumber() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("8,888", b.formatNumber(8888));
            assertEquals("2,500.98", b.formatDecimal(new BigDecimal("2500.98")));
            assertEquals("€3,500.00", b.formatCurrency(3500, "EUR"));
            assertEquals("64%", b.formatPercent(0.64));
            assertEquals("2.5E3", b.formatScientific(2500));
        }
    }
}