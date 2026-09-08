package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultUnionTest {

    static Object f(Object input) {
        if (input instanceof String) return ((String)input).toUpperCase();
        if (input instanceof Integer) return (Integer)input * 5;
        if (input instanceof Double) return -((Double)input);
        return null;
    }

    @Test
    void testUnionString() {
        assertEquals("XYZ", f("xyz"));
    }

    @Test
    void testUnionInt() {
        assertEquals(80, f(16));
    }

    @Test
    void testUnionDouble() {
        assertEquals(-3.0, (Double)f(3.0), 1e-9);
    }
}