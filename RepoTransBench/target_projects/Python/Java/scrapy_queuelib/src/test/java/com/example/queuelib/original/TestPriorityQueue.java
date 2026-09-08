package com.example.queuelib.original;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.PriorityQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPriorityQueue {

    @Test
    void testPriorityPushPopOrder() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("one"), 2);
        pq.push(b("zero"), 1);
        pq.push(b("five"), 5);
        pq.push(b("three"), 3);

        assertArrayEquals(b("zero"), pq.pop());
        assertArrayEquals(b("one"), pq.pop());
        assertArrayEquals(b("three"), pq.pop());
        assertArrayEquals(b("five"), pq.pop());
        assertNull(pq.pop());
        pq.close();
    }

    @Test
    void testPriorityQueuePeek() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("bar"), 2);
        pq.push(b("foo"), 1);
        assertArrayEquals(b("foo"), pq.peek());
        assertArrayEquals(b("foo"), pq.pop());
        assertArrayEquals(b("bar"), pq.peek());
        pq.close();
    }

    @Test
    void testPriorityQueueMultipleSamePriority() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("first_a"), 1);
        pq.push(b("second_a"), 1);
        pq.push(b("first_b"), 2);
        assertArrayEquals(b("first_a"), pq.pop());
        assertArrayEquals(b("second_a"), pq.pop());
        assertArrayEquals(b("first_b"), pq.pop());
        pq.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}