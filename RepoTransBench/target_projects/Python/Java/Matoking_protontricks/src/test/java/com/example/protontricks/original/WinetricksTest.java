package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class WinetricksTest {

    static class Winetricks {
        static boolean isAvailable() { return true; }  // For test
        static String getVersion() { return "20240101"; }
    }

    @Test
    void testIsAvailable() {
        assertTrue(Winetricks.isAvailable());
    }

    @Test
    void testGetVersion() {
        String v = Winetricks.getVersion();
        assertTrue(v.matches("\\d+"));
    }
}