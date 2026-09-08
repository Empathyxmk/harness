package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TimerExtraTest {
    @Test
    public void testNanoTimer() {
        long before = System.nanoTime();
        for (int i = 0; i < 1000000; i++) {}
        long after = System.nanoTime();
        assertTrue(after > before);
    }
}