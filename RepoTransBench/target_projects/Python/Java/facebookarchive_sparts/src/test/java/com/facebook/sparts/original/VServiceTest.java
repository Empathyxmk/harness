package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class VServiceTest {
    static class OrigTestService {
        public static String[] TASKS = {"taskA", "taskB"};
    }

    @Test
    public void testTasksAttribute() {
        assertArrayEquals(new String[]{"taskA", "taskB"}, OrigTestService.TASKS);
    }

    @Test
    public void testInitFromCLIExists() {
        class VService {
            public void initFromCLI() {}
        }
        assertDoesNotThrow(() -> {
            VService v = new VService();
            v.initFromCLI();
        });
    }
}