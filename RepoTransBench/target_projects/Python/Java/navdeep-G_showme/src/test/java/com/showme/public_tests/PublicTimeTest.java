package com.showme.public_tests;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicTimeTest {
    @Test
    void testTimeTypeAndRange() {
        double value = Core.time();
        assertTrue(value < 100000);
        assertTrue(value >= 0.0);
    }
}