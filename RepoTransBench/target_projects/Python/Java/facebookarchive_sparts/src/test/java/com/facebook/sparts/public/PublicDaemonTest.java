package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDaemonTest {
    @Test
    public void testPublicDaemonPlaceholder1() {
        assertEquals(84, 42*2);
    }

    @Test
    public void testPublicDaemonPlaceholder2() {
        String sep = System.getProperty("file.separator");
        assertTrue(sep.equals("/") || sep.equals("\\"));
    }

    @Test
    public void testPublicDaemonPlaceholder3() {
        int[] a = {1, 3, 5};
        int sum = 0;
        for (int v : a) sum += v*v;
        assertEquals(35, sum);
    }
}