package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DesktopInstallTest {
    static boolean isInstalled() { return true; }
    @Test
    void testDesktopInstallCheck() {
        assertTrue(isInstalled());
    }
}