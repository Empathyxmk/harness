package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import java.util.LinkedList;
import java.util.Queue;

import static org.junit.jupiter.api.Assertions.*;

public class QueueTest {
    @Test
    public void testQueueOfferPollSize() {
        Queue<Integer> q = new LinkedList<>();
        assertTrue(q.isEmpty());
        q.offer(1);
        q.offer(2);
        assertFalse(q.isEmpty());
        assertEquals(2, q.size());
        assertEquals(1, q.poll());
        assertEquals(2, q.poll());
        assertTrue(q.isEmpty());
    }
}