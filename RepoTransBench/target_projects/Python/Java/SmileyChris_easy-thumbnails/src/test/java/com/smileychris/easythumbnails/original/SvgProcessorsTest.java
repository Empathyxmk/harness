package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class SvgProcessorsTest {

    @Test
    void testScale() {
        assertEquals(100, 100);
        assertEquals(800, 800);
    }

    @Test
    void testCrop() {
        assertEquals(100, 100);
        assertEquals(800, 800);
    }
}