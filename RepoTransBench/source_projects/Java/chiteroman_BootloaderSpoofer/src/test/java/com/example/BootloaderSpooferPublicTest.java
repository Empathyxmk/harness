package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BootloaderSpooferPublicTest {

    @Test
    public void testToggleSpoofState() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        // Sequence: spoof, reset, spoof
        bs.spoof();
        assertTrue(bs.isSpoofed());
        assertEquals("Spoofed", bs.status());
        bs.reset();
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
        bs.spoof();
        assertTrue(bs.isSpoofed());
        assertEquals("Spoofed", bs.status());
    }

    @Test
    public void testMultipleReset() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        // Try resetting before spoofing, then after spoofing
        bs.reset(); // should remain Not spoofed
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
        bs.spoof();
        assertTrue(bs.isSpoofed());
        bs.reset();
        bs.reset(); // should stay Not spoofed after two resets
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
    }

    @Test
    public void testAlternatingSpoofAndReset() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        // Spoof -> Reset -> Spoof -> Reset
        bs.spoof();
        assertTrue(bs.isSpoofed());
        bs.reset();
        assertFalse(bs.isSpoofed());
        bs.spoof();
        assertTrue(bs.isSpoofed());
        bs.reset();
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
    }

    @Test
    public void testRepeatedResetWithoutSpoof() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        bs.reset();
        bs.reset();
        // Never spoofed
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
        // Now spoof and test again
        bs.spoof();
        assertTrue(bs.isSpoofed());
        bs.reset();
        assertFalse(bs.isSpoofed());
    }
}