package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestSkippingTest {

    @Test
    void testHeavyCalculation() {
        // simulate skipping with an early return for demo purposes, as @Disabled could be used
        if (System.getProperty("skipHeavy", "false").equals("true")) return;
        assertEquals(10, 5+5);
    }

    @Test
    void testRegular() {
        assertEquals(4, 2+2);
    }
}