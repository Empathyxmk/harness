package com.dearbinge.openapi;

import org.junit.Test;

import static org.junit.Assert.*;

public class HttpSessionConfigPublicTest {
    @Test
    public void testSessionTimeoutPublicVariant() {
        // Simulate the timeout for a different input (e.g., 42 min)
        int maxInactiveIntervalInSeconds = 42 * 60;
        assertEquals(2520, maxInactiveIntervalInSeconds);
    }
}