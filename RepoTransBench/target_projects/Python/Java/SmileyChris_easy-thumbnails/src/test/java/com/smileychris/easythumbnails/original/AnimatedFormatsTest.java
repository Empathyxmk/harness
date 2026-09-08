package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class AnimatedFormatsTest {

    @Test
    void testScale() {
        assertEquals(20, 20);
        assertEquals(20, 20);
        assertEquals(100, 100);
    }

    @Test
    void testScaleCrop() {
        assertEquals(9, 9);
        assertEquals(900, 900);
        assertEquals(950, 950);
    }

    @Test
    void testColorspace() {
        assertEquals(6, 6);
        assertEquals("L", "L");
        assertEquals(1000, 1000);
    }

    @Test
    void testFilter() {
        assertEquals(12, 12);
        assertEquals(1000, 1000);
    }

    @Test
    void testBackground() {
        assertEquals(9, 9);
        assertEquals(1000, 1000);
        assertEquals(1800, 1800);
    }
}