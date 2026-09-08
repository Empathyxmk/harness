package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TimerTest {
    @Test
    public void testSystemTimer() {
        long start = System.currentTimeMillis();
        try {
            Thread.sleep(12);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        assertTrue(System.currentTimeMillis() >= start);
    }
}