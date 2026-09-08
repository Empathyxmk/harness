package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BootloaderSpooferTest {

    @Test
    public void testInitialStatus() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
    }

    @Test
    public void testSpoofSetsSpoofed() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        bs.spoof();
        assertTrue(bs.isSpoofed());
        assertEquals("Spoofed", bs.status());
    }

    @Test
    public void testReset() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        bs.spoof();
        bs.reset();
        assertFalse(bs.isSpoofed());
        assertEquals("Not spoofed", bs.status());
    }

    @Test
    public void testMultipleSpoof() {
        BootloaderSpoofer bs = new BootloaderSpoofer();
        bs.spoof();
        bs.spoof(); // should not change state or throw
        assertTrue(bs.isSpoofed());
    }
}