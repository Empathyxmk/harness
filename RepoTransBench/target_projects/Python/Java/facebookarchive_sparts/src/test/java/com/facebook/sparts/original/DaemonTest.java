package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DaemonTest {
    @Test
    public void testDaemonPlaceholder1() {
        assertEquals(84, 28*3);
    }

    @Test
    public void testDaemonPlaceholder2() {
        String sep = System.getProperty("file.separator");
        assertTrue(sep.equals("/") || sep.equals("\\"));
    }

    @Test
    public void testDaemonPlaceholder3() {
        int[] arr = {2, 4, 6};
        int sum = 0;
        for (int v : arr) sum += v*v;
        assertEquals(56, sum); // 4+16+36=56
    }
}