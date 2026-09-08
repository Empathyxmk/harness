package com.navdeepg.samplemod.public_tests;

import com.navdeepg.samplemod.core.Core;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicAdvanced {

    @Test
    void testSafeDivideNormalPublic() {
        assertEquals(5, Core.safeDivide(15, 3));
    }

    @Test
    void testSafeDivideNegativePublic() {
        assertEquals(-3, Core.safeDivide(-9, 3));
    }

    @Test
    void testSafeDivideZeroDividendPublic() {
        assertEquals(0, Core.safeDivide(0, 2));
    }

    @Test
    void testSafeDivideRaisesZeroDivisionPublic() {
        Exception e = assertThrows(ArithmeticException.class, () -> Core.safeDivide(2, 0));
        // Optional: check if the message contains "zero"
        assertTrue(e.getMessage() == null || e.getMessage().toLowerCase().contains("zero"));
    }
}