package com.example.queuelib.original;

import com.example.queuelib.BaseQueue;
import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.LifoMemoryQueue;
import com.example.queuelib.PriorityQueue;
import com.example.queuelib.RoundRobinQueue;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicApi {

    @Test
    void testFifoMemoryQueueImplementsBaseQueue() {
        FifoMemoryQueue<byte[]> q = new FifoMemoryQueue<>();
        q.push(b("foo"));
        assertTrue(q instanceof BaseQueue);
        q.close();
    }

    @Test
    void testLifoMemoryQueueImplementsBaseQueue() {
        LifoMemoryQueue<byte[]> q = new LifoMemoryQueue<>();
        q.push(b("baz"));
        assertTrue(q instanceof BaseQueue);
        q.close();
    }

    @Test
    void testPriorityQueueIsBaseQueue() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("one"), 1);
        assertTrue(pq instanceof BaseQueue);
        pq.close();
    }

    @Test
    void testRoundRobinQueueIsBaseQueue() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(k -> new FifoMemoryQueue<>());
        rrq.push(b("alpha"), "1");
        assertTrue(rrq instanceof BaseQueue);
        rrq.close();
    }

    // Test basic expected BaseQueue API contract
    @Test
    void testBaseQueueApiContract() {
        class TestQueue<T> implements BaseQueue<T> {
            private final java.util.LinkedList<T> l = new java.util.LinkedList<>();
            @Override public void push(T obj) { l.add(obj); }
            @Override public T pop() { return l.isEmpty() ? null : l.removeFirst(); }
            @Override public T peek() { return l.isEmpty() ? null : l.getFirst(); }
            @Override public void close() { l.clear(); }
            @Override public int size() { return l.size(); }
        }
        TestQueue<byte[]> q = new TestQueue<>();
        q.push(b("bob"));
        assertEquals(b("bob")[0], q.peek()[0]);
        assertTrue(q instanceof BaseQueue);
        q.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}