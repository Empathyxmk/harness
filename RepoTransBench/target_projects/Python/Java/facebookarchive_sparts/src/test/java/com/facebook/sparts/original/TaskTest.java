package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TaskTest {
    interface FancyTask {
        int foo();
        void bar(int x);
    }

    static class MyTask implements FancyTask {
        int state = 0;
        public int foo() { return 7; }
        public void bar(int x) { state += x; }
    }

    @Test
    public void testMyTask() {
        MyTask t = new MyTask();
        assertEquals(7, t.foo());
        t.bar(5);
        assertEquals(5, t.state);
        t.bar(9);
        assertEquals(14, t.state);
    }
}