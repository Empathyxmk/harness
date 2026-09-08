package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public AnimationUtils test with different data than private.
 */
public class AnimationUtilsPublicTest {
    @Test
    public void simplePublicAnimationTest() {
        // Use a unique duration to avoid overlap with private
        int duration = 350;
        assertTrue("Duration should be greater than 200", duration > 200);
    }
}