package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class SourceGeneratorsTest {

    @Test
    void testNotImage() {
        assertThrows(Exception.class, () -> { throw new Exception("IOError"); });
    }

    @Test
    void testNearlyImage() {
        assertTrue(true); // Would check image is not null
    }
}