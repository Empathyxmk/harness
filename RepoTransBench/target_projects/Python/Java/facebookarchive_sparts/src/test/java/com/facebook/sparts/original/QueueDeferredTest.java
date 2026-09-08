package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import java.util.ArrayDeque;
import java.util.Deque;

import static org.junit.jupiter.api.Assertions.*;

public class QueueDeferredTest {
    @Test
    public void testDequePushPop() {
        Deque<String> d = new ArrayDeque<>();
        d.push("A");
        d.push("B");
        assertEquals("B", d.pop());
        assertEquals("A", d.pop());
        assertTrue(d.isEmpty());
    }
}