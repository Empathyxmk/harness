package com.luckysj.threadpool;

import com.luckysj.threadpool.core.ThreadPool;
import com.luckysj.threadpool.policy.impl.AbortPolicy;
import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class MainPublicTest {

    @Test
    public void publicThreadPoolTest() throws InterruptedException {
        AtomicInteger sum = new AtomicInteger(0);
        ThreadPool pool = new ThreadPool(
                2,     // core size (changed from default for public test)
                3,     // queue capacity
                4,     // max pool size
                1000,  // keep alive (ms)
                new AbortPolicy(),
                "PublicTestPool"
        );

        int numberOfTasks = 7; // different task count than sample
        for (int i = 0; i < numberOfTasks; i++) {
            final int index = i;
            pool.execute(() -> sum.addAndGet(index));
        }

        pool.shutdown();
        while (!pool.isTerminated()) {
            Thread.sleep(10);
        }

        int expected = 0;
        for (int i = 0; i < numberOfTasks; i++) {
            expected += i;
        }
        assertEquals(expected, sum.get());
    }
}