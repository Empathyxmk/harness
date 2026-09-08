package com.example.queuelib.original;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.RoundRobinQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestRoundRobinQueue {

    @Test
    void testRoundRobinPushPop() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(key -> new FifoMemoryQueue<>());
        rrq.push(b("a1"), "alpha");
        rrq.push(b("b1"), "beta");
        rrq.push(b("a2"), "alpha");
        rrq.push(b("g1"), "gamma");
        rrq.push(b("b2"), "beta");

        // The queue alternates between keys, popping one element from each in order of keys seen
        // order: alpha, beta, gamma, alpha, beta

        assertArrayEquals(b("a1"), rrq.pop());
        assertArrayEquals(b("b1"), rrq.pop());
        assertArrayEquals(b("g1"), rrq.pop());
        assertArrayEquals(b("a2"), rrq.pop());
        assertArrayEquals(b("b2"), rrq.pop());
        assertNull(rrq.pop());
        rrq.close();
    }

    @Test
    void testRoundRobinQueuePeek() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(key -> new FifoMemoryQueue<>());
        rrq.push(b("foo"), "first");
        rrq.push(b("bar"), "second");
        assertArrayEquals(b("foo"), rrq.peek());
        // Now advance one, so "bar" is at the front in round robin
        rrq.pop();
        assertArrayEquals(b("bar"), rrq.peek());
        rrq.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}