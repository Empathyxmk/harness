package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TornadoTest {
    @Test
    public void testTornadoLoop() {
        int val = 12;
        for (int i = 0; i < 5; i++) val += i;
        assertEquals(22, val);
    }
}