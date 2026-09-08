package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultPrimitiveTest {

    @Test
    void testInt() {
        int x = 444;
        assertEquals(444, x);
    }

    @Test
    void testBool() {
        boolean b = true;
        assertTrue(b);
        b = false;
        assertFalse(b);
    }

    @Test
    void testFloat() {
        double f = 3.1456;
        assertEquals(3.1456, f, 1e-9);
    }

    @Test
    void testChar() {
        char c = 'z';
        assertEquals('z', c);
    }
}