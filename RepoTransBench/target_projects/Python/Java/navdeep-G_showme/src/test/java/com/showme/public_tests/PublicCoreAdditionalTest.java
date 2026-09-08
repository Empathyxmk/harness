package com.showme.public_tests;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicCoreAdditionalTest {
    @Test
    void testAdditionalFunctionality() {
        assertEquals("TESTING", Core.upper("testing"));
        assertEquals(122, Core.add(101, 21));
        assertEquals(31, Core.subtract(45, 14));
        assertEquals(52, Core.multiply(13, 4));
        assertEquals(20.0, Core.divide(80, 4));
        assertEquals(15.4, Core.divide(77, 5), 1e-8);
        assertEquals(-7, Core.add(-5, -2));
    }
}