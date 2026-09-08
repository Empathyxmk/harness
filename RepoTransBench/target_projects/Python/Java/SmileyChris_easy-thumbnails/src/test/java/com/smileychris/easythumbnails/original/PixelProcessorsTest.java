package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PixelProcessorsTest {

    @Test
    void testScale() {
        assertEquals(100, 100);
        assertEquals(800, 800);
        assertEquals(1000, 1000);
    }

    @Test
    void testCrop() {
        assertEquals(100, 100);
        assertEquals(800, 800);
    }
}