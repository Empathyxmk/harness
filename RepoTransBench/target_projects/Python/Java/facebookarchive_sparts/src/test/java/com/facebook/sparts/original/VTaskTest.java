package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class VTaskTest {
    interface DummyTask {
        String getName();
        int run();
    }

    static class MyDummyTask implements DummyTask {
        public String getName() {
            return "taskname";
        }
        public int run() {
            return 123;
        }
    }

    @Test
    public void testDummyTask() {
        MyDummyTask t = new MyDummyTask();
        assertEquals("taskname", t.getName());
        assertEquals(123, t.run());
    }
}