package com.nhm.pyzbar.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestInit {
    @Test
    void testVersionExists() {
        // Simulate Pyzbar class with __version__ member
        try {
            Class<?> pyzbar = Class.forName("com.nhm.pyzbar.Pyzbar");
            assertNotNull(pyzbar.getDeclaredField("__version__"));
            assertTrue(pyzbar.getDeclaredField("__version__").getType() == String.class);
        } catch (Exception e) {
            fail("Pyzbar class must have a '__version__' field of type String: " + e);
        }
    }
}