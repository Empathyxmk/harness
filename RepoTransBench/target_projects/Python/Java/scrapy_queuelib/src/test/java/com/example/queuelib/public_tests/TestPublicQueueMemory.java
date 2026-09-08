package com.example.queuelib.public_tests;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.LifoMemoryQueue;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicQueueMemory {

    @Test
    void testFifoQueue() {
        FifoMemoryQueue<byte[]> q = new FifoMemoryQueue<>();
        q.push(b("cat"));
        q.push(b("dog"));
        assertArrayEquals(b("cat"), q.pop());
        assertArrayEquals(b("dog"), q.pop());
        assertNull(q.pop());
        q.close();
    }

    @Test
    void testLifoQueue() {
        LifoMemoryQueue<byte[]> q = new LifoMemoryQueue<>();
        q.push(b("cat"));
        q.push(b("dog"));
        assertArrayEquals(b("dog"), q.pop());
        assertArrayEquals(b("cat"), q.pop());
        assertNull(q.pop());
        q.close();
    }

    @Test
    void testPeekBehavior() {
        FifoMemoryQueue<byte[]> q = new FifoMemoryQueue<>();
        q.push(b("ant"));
        assertArrayEquals(b("ant"), q.peek());
        assertArrayEquals(b("ant"), q.pop());
        assertNull(q.peek());
        q.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}