package com.luckysj.demo.concurrent;

import org.junit.jupiter.api.Test;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Public version: Test simulated concurrency at a different scale/input.
 */
public class ConcurrencePublicTest {

    @Test
    public void testLowerConcurrency() throws InterruptedException {
        final AtomicInteger atomicInteger = new AtomicInteger(0);
        final int nThreads = 5;
        final int nTasks = 20; // fewer tasks for public, different from 1000
        final int increments = 10; // each increments 10 times, modified for demonstration
        final CountDownLatch latchReady = new CountDownLatch(nTasks);
        final CountDownLatch latchDone = new CountDownLatch(nTasks);
        ExecutorService executor = Executors.newFixedThreadPool(nThreads);

        for (int i = 0; i < nTasks; i++) {
            executor.submit(() -> {
                try {
                    latchReady.await();
                } catch (InterruptedException ignored) {}
                for (int j = 0; j < increments; j++) {
                    atomicInteger.incrementAndGet();
                }
                latchDone.countDown();
            });
            latchReady.countDown();
        }

        latchDone.await();
        executor.shutdown();
        assertEquals(nTasks * increments, atomicInteger.get());
    }
}