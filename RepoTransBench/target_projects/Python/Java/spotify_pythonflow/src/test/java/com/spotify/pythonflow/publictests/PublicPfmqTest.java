package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.concurrent.atomic.AtomicInteger;

public class PublicPfmqTest {

    static class Task implements Runnable {
        AtomicInteger state = new AtomicInteger(0);
        @Override
        public void run() {
            state.incrementAndGet();
        }
    }

    @Test
    public void testPublicTaskRun() {
        Task t = new Task();
        assertEquals(0, t.state.get());
        t.run();
        assertEquals(1, t.state.get());
    }
}