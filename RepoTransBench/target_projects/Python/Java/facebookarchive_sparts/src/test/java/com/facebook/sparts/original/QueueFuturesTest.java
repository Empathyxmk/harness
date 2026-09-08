package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;

public class QueueFuturesTest {
    @Test
    public void testFutureValues() throws Exception {
        ExecutorService exec = Executors.newFixedThreadPool(1);
        Future<String> fut = exec.submit(() -> "hello");
        assertEquals("hello", fut.get(2, TimeUnit.SECONDS));
        exec.shutdown();
    }
}