package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PollerTest {
    static class DummyPoller {
        boolean polled = false;
        public boolean poll() {
            polled = !polled;
            return polled;
        }
    }

    @Test
    public void testPollerAlternates() {
        DummyPoller poller = new DummyPoller();
        assertTrue(poller.poll());
        assertFalse(poller.poll());
        assertTrue(poller.poll());
    }
}