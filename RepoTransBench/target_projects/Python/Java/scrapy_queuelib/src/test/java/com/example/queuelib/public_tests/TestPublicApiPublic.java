package com.example.queuelib.public_tests;

import com.example.queuelib.BaseQueue;
import com.example.queuelib.FifoMemoryQueue;
import com.example.queuelib.LifoMemoryQueue;
import com.example.queuelib.PriorityQueue;
import com.example.queuelib.RoundRobinQueue;
import org.junit.jupiter.api.Test;

import java.util.LinkedList;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicApiPublic {

    @Test
    void testFifoMemoryQueueApiSurface() {
        FifoMemoryQueue<byte[]> q = new FifoMemoryQueue<>();
        q.push(b("A"));
        q.close();
        assertTrue(q instanceof BaseQueue);
    }

    @Test
    void testLifoMemoryQueueApiSurface() {
        LifoMemoryQueue<byte[]> q = new LifoMemoryQueue<>();
        q.push(b("A"));
        q.close();
        assertTrue(q instanceof BaseQueue);
    }

    @Test
    void testPriorityQueueApiSurface() {
        PriorityQueue<byte[]> pq = new PriorityQueue<>(prio -> new FifoMemoryQueue<>());
        pq.push(b("A"), 1);
        pq.close();
        assertTrue(pq instanceof BaseQueue);
    }

    @Test
    void testRoundRobinQueueApiSurface() {
        RoundRobinQueue<byte[]> rrq = new RoundRobinQueue<>(key -> new FifoMemoryQueue<>());
        rrq.push(b("B"), "alpha");
        rrq.close();
        assertTrue(rrq instanceof BaseQueue);
    }

    @Test
    void testCustomMemoryQueueApiSurface() {
        class MyMemoryQueue<T> implements BaseQueue<T> {
            final LinkedList<T> items = new LinkedList<>();
            @Override
            public void push(T obj) { items.add(obj); }
            @Override
            public T pop() { return items.isEmpty() ? null : items.removeFirst(); }
            @Override
            public T peek() { return items.isEmpty() ? null : items.getFirst(); }
            @Override
            public void close() { items.clear(); }
            @Override
            public int size() { return items.size(); }
        }
        MyMemoryQueue<byte[]> q = new MyMemoryQueue<>();
        q.push(b("bob"));
        assertEquals(b("bob")[0], q.peek()[0]);
        assertTrue(q instanceof BaseQueue);
        q.close();
    }

    private static byte[] b(String s) {
        return s.getBytes();
    }
}