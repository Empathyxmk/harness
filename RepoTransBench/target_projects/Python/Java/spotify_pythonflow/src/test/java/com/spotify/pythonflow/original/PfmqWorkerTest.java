package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PfmqWorkerTest {

    static class TestWorker {
        private boolean running = false;
        public void start() { running = true; }
        public void stop() { running = false; }
        public boolean isRunning() { return running; }
    }

    @Test
    public void testStartStopWorker() {
        TestWorker w = new TestWorker();
        assertFalse(w.isRunning());
        w.start();
        assertTrue(w.isRunning());
        w.stop();
        assertFalse(w.isRunning());
    }
}