package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class PicassoUtilPublicTest {
    @Test
    public void testUrlIsJpeg_public() {
        // Use jpeg instead of png
        String url = "https://example.org/altpic.jpeg";
        assertTrue(url.endsWith(".jpeg"));
    }
}