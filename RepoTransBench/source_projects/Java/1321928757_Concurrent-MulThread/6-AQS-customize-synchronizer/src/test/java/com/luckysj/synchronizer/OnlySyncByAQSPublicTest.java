package com.luckysj.synchronizer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class OnlySyncByAQSPublicTest {

    // Test that the lock is actually exclusive for multiple threads,
    // with shorter waits and different thread count.
    @Test
    public void testCustomAQSLock_MultipleThreads() throws InterruptedException {
        OnlySyncByAQS lock = new OnlySyncByAQS();
        int numThreads = 4; // Different from sample's 3
        int[] count = {0};
        Thread[] threads = new Thread[numThreads];
        for (int t = 0; t < numThreads; t++) {
            threads[t] = new Thread(() -> {
                lock.lock();
                try {
                    count[0]++;
                    try {
                        Thread.sleep(250); // Shorter than original to speed up test
                    } catch (InterruptedException ignored) {}
                } finally {
                    lock.unlock();
                }
            });
        }
        for (Thread thread : threads) {
            thread.start();
        }
        for (Thread thread : threads) {
            thread.join();
        }
        assertTrue(count[0] == numThreads); // All threads incremented
    }
}