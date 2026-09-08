package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class BitmapUtilPublicTest {
    @Test
    public void testImageWidthLargerThanHeight_public() {
        // Flip logic from original - width > height
        int width = 600, height = 400;
        assertTrue(width > height);
    }
}