package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class EngineTest {

    @Test
    void testSaveJpegRgba() {
        assertEquals("RGB", "RGB");
    }

    @Test
    void testSaveJpegLa() {
        assertEquals("L", "L");
    }

    @Test
    void testSaveWithIccProfile() {
        assertNotNull("something");
    }
}