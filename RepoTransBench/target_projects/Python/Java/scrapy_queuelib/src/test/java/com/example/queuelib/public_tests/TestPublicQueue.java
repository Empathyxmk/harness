package com.example.queuelib.public_tests;

import com.example.queuelib.BaseQueue;
import org.junit.jupiter.api.Test;

import java.util.LinkedList;

import static org.junit.jupiter.api.Assertions.*;

class TestMemoryQueue<T> implements BaseQueue<T> {
    private final LinkedList<T> items = new LinkedList<>();
    private boolean closed = false;

    @Override
    public void push(T obj) {
        if (closed) throw new IllegalStateException("Queue closed");
        items.add(obj);
    }

    @Override
    public T pop() {
        if (closed) throw new IllegalStateException("Queue closed");
        return items.isEmpty() ? null : items.removeFirst();
    }

    @Override
    public T peek() {
        if (closed) throw new IllegalStateException("Queue closed");
        return items.isEmpty() ? null : items.getFirst();
    }

    @Override
    public void close() {
        closed = true;
        items.clear();
    }

    @Override
    public int size() {
        return closed ? 0 : items.size();
    }
}

public class TestPublicQueue {

    @Test
    void testPushPopPeekAndSize() {
        TestMemoryQueue<byte[]> q = new TestMemoryQueue<>();
        assertEquals(0, q.size());
        q.push(b("cat"));
        assertEquals(1, q.size());
        assertArrayEquals(b("cat"), q.peek());
        assertArrayEquals(b("cat"), q.pop());
        assertNull(q.peek());
        assertEquals(0, q.size());
    }

    @Test
    void testErrorAfterClose() {
        TestMemoryQueue<byte[]> q = new TestMemoryQueue<>();
        q.push(b("octopus"));
        q.close();
        assertThrows(IllegalStateException.class, () -> q.push(b("dolphin")));
        assertThrows(IllegalStateException.class, q::pop);
        assertThrows(IllegalStateException.class, q::peek);
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}