package com.example.queuelib.public_tests;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.PriorityQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicPriorityQueue {

    @Test
    void testPushPopOrder() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("b"), 2);
        pq.push(b("a"), 1);
        pq.push(b("c"), 3);
        assertArrayEquals(b("a"), pq.pop());
        assertArrayEquals(b("b"), pq.pop());
        assertArrayEquals(b("c"), pq.pop());
        assertNull(pq.pop());
        pq.close();
    }

    @Test
    void testPeek() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("alpha"), 0);
        pq.push(b("beta"), 15);
        assertArrayEquals(b("alpha"), pq.peek());
        pq.pop();
        assertArrayEquals(b("beta"), pq.peek());
        pq.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}