package com.nhm.pyzbar.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Java translation of test_init.py
 */
public class TestInitCoverage {
    @Test
    void testVersionExists() {
        try {
            Class<?> pyzbar = Class.forName("com.nhm.pyzbar.Pyzbar");
            assertTrue(pyzbar.getDeclaredField("__version__").getType() == String.class);
            // Some Java "pyzbar" class should have static __version__ field
            // and type String.
        } catch (Exception e) {
            fail("Pyzbar must contain static String __version__");
        }
    }
}