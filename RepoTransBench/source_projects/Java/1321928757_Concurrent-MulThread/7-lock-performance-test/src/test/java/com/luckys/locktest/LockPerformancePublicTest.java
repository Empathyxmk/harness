package com.luckys.locktest;

import org.junit.jupiter.api.Test;

import java.util.concurrent.locks.ReentrantLock;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class LockPerformancePublicTest {

    /**
     * Public test: lock and unlock a ReentrantLock with different iteration count.
     */
    @Test
    public void testReentrantLockLowContention() {
        ReentrantLock lock = new ReentrantLock();
        int sum = 0;
        int N = 50; // Different from any original value
        for (int i = 0; i < N; i++) {
            lock.lock();
            try {
                sum += i;
            } finally {
                lock.unlock();
            }
        }
        assertTrue(sum > 0);
    }
}