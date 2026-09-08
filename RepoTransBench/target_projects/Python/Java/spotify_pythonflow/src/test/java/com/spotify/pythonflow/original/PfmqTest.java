package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class PfmqTest {

    public static class DummyTask implements Runnable {
        private final AtomicInteger executed;
        private final int expected;
        public DummyTask(AtomicInteger executed, int expected) {
            this.executed = executed;
            this.expected = expected;
        }
        @Override
        public void run() {
            executed.incrementAndGet();
            assertEquals(expected, executed.get());
        }
    }

    @Test
    public void testTaskExecutionOnce() {
        AtomicInteger executed = new AtomicInteger(0);
        DummyTask t = new DummyTask(executed, 1);
        t.run();
        assertEquals(1, executed.get());
    }

    @Test
    public void testWorkerStop() {
        DummyWorker w = new DummyWorker();
        w.start();
        assertFalse(w.isStopped.get());
        w.stop();
        assertTrue(w.isStopped.get());
        assertTrue(w.stoppedMethodCalled.get());
    }

    static class DummyWorker {
        final AtomicBoolean isStopped = new AtomicBoolean(false);
        final AtomicBoolean stoppedMethodCalled = new AtomicBoolean(false);

        public void start() {
            isStopped.set(false);
        }
        public void stop() {
            isStopped.set(true);
            stoppedMethodCalled.set(true);
        }
    }
}