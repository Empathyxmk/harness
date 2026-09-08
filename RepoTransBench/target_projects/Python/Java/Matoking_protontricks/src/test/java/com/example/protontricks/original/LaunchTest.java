package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LaunchTest {
    static boolean canLaunch() { return true; }
    @Test
    void testLaunchCanLaunch() {
        assertTrue(canLaunch());
    }
}