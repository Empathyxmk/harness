package com.example.queuelib.original;

import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.LifoMemoryQueue;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestQueueMemory {

    @Test
    void testFifoQueueOrdering() {
        FifoMemoryQueue<byte[]> fifo = new FifoMemoryQueue<>();
        fifo.push(b("foo"));
        fifo.push(b("bar"));
        assertArrayEquals(b("foo"), fifo.pop());
        assertArrayEquals(b("bar"), fifo.pop());
        assertNull(fifo.pop());
        fifo.close();
    }

    @Test
    void testFifoQueuePeek() {
        FifoMemoryQueue<byte[]> fifo = new FifoMemoryQueue<>();
        fifo.push(b("foo"));
        assertArrayEquals(b("foo"), fifo.peek());
        assertArrayEquals(b("foo"), fifo.pop());
        assertNull(fifo.peek());
        fifo.close();
    }

    @Test
    void testLifoQueueOrdering() {
        LifoMemoryQueue<byte[]> lifo = new LifoMemoryQueue<>();
        lifo.push(b("foo"));
        lifo.push(b("bar"));
        assertArrayEquals(b("bar"), lifo.pop());
        assertArrayEquals(b("foo"), lifo.pop());
        assertNull(lifo.pop());
        lifo.close();
    }

    @Test
    void testLifoQueuePeek() {
        LifoMemoryQueue<byte[]> lifo = new LifoMemoryQueue<>();
        lifo.push(b("foo"));
        lifo.push(b("bar"));
        assertArrayEquals(b("bar"), lifo.peek());
        assertArrayEquals(b("bar"), lifo.pop());
        assertArrayEquals(b("foo"), lifo.pop());
        assertNull(lifo.peek());
        lifo.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}