package com.facebook.sparts.original.tasks;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ThriftMultiplexedTest {
    @Test
    public void testMultiplexedThriftDummy() {
        assertNotNull("multiplexed".toUpperCase());
        assertTrue("multiplexed".length() > 5);
        assertEquals("MULTIPLEXED", "multiplexed".toUpperCase());
    }
}