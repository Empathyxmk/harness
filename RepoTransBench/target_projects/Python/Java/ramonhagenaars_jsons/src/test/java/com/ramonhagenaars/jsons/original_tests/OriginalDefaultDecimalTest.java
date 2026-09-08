package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultDecimalTest {

    @Test
    void testDecimalEquality() {
        BigDecimal d1 = new BigDecimal("123.45");
        BigDecimal d2 = new BigDecimal("123.4500");
        assertEquals(0, d1.compareTo(d2));
    }

    @Test
    void testDecimalToString() {
        BigDecimal d = new BigDecimal("789.000001");
        assertEquals("789.000001", d.toString());
    }
}