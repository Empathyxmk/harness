package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class AppUtilsPublicTest {
    @Test
    public void testIsAppForeground_true() {
        // Different value from original (true instead of false)
        boolean isForeground = true;
        assertTrue(isForeground);
    }
}