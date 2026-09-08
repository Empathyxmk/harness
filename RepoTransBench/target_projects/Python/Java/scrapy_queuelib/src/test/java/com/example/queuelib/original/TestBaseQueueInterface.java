package com.example.queuelib.original;

import com.example.queuelib.BaseQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.LinkedList;

public class TestBaseQueueInterface {

    static class DummyQueue<T> implements BaseQueue<T> {
        private final LinkedList<T> list = new LinkedList<>();
        private boolean closed = false;
        @Override public void push(T o) { if (closed) throw new IllegalStateException(); list.add(o); }
        @Override public T pop() { if (closed) throw new IllegalStateException(); return list.isEmpty() ? null : list.removeFirst(); }
        @Override public T peek() { if (closed) throw new IllegalStateException(); return list.isEmpty() ? null : list.getFirst(); }
        @Override public void close() { closed = true; list.clear(); }
        @Override public int size() { if (closed) return 0; return list.size(); }
    }

    @Test
    void testPushPopPeekAndSize() {
        DummyQueue<byte[]> q = new DummyQueue<>();
        assertEquals(0, q.size());
        q.push(b("snail"));
        assertEquals(1, q.size());
        assertArrayEquals(b("snail"), q.peek());
        assertArrayEquals(b("snail"), q.pop());
        assertNull(q.peek());
        assertEquals(0, q.size());
    }

    @Test
    void testErrorOnUseAfterClose() {
        DummyQueue<byte[]> q = new DummyQueue<>();
        q.push(b("hippo"));
        q.close();
        assertThrows(IllegalStateException.class, () -> q.push(b("platypus")));
        assertThrows(IllegalStateException.class, q::pop);
        assertThrows(IllegalStateException.class, q::peek);
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}