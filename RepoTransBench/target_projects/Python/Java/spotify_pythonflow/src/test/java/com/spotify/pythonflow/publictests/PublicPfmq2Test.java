package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicPfmq2Test {

    static class Task implements Runnable {
        boolean wasRun = false;
        @Override
        public void run() {
            wasRun = true;
        }
    }

    @Test
    public void testPublicTaskRunEmpty() {
        Task t = new Task();
        assertFalse(t.wasRun);
        t.run();
        assertTrue(t.wasRun);
    }
}