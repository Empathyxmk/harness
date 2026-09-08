package com.example.queuelib.public_tests;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.RoundRobinQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicRoundRobinQueue {

    @Test
    void testPushPopOrder() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(k -> new FifoMemoryQueue<>());
        rrq.push(b("a"), "k1");
        rrq.push(b("b"), "k2");
        rrq.push(b("c"), "k1");
        rrq.push(b("d"), "k2");

        assertArrayEquals(b("a"), rrq.pop());
        assertArrayEquals(b("b"), rrq.pop());
        assertArrayEquals(b("c"), rrq.pop());
        assertArrayEquals(b("d"), rrq.pop());
        assertNull(rrq.pop());
        rrq.close();
    }

    @Test
    void testPeek() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(k -> new FifoMemoryQueue<>());
        rrq.push(b("x"), "g");
        rrq.push(b("y"), "f");
        assertArrayEquals(b("x"), rrq.peek());
        rrq.pop();
        assertArrayEquals(b("y"), rrq.peek());
        rrq.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}