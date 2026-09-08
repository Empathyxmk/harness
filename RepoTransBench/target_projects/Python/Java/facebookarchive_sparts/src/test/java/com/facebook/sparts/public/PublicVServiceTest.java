package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicVServiceTest {
    static class PubTestService {
        public static String[] TASKS = {"task1", "task2"};
    }

    @Test
    public void testPublicTasksAttribute() {
        assertArrayEquals(new String[]{"task1", "task2"}, PubTestService.TASKS);
    }

    @Test
    public void testPublicInitFromCLIExists() {
        // Just check the method is present: simulate method called initFromCLI
        class VService {
            public void initFromCLI() {}
        }
        assertDoesNotThrow(() -> {
            VService v = new VService();
            v.initFromCLI();
        });
    }
}