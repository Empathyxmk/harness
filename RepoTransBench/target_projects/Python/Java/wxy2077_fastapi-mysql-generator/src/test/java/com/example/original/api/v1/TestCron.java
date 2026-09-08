package com.example.original.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestCron {

    static class CronJob {
        String name;
        boolean active;
        CronJob(String name) { this.name = name; this.active = true; }
    }

    static Map<String, CronJob> jobs = new HashMap<>();

    @BeforeEach
    void setup() {
        jobs.clear();
        jobs.put("job1", new CronJob("job1"));
    }

    @Test
    void testAddJob() {
        jobs.put("job2", new CronJob("job2"));
        assertTrue(jobs.containsKey("job2"), "Should add and find job2");
    }

    @Test
    void testRemoveJob() {
        jobs.remove("job1");
        assertFalse(jobs.containsKey("job1"), "Should remove job1");
    }

    @Test
    void testJobActive() {
        assertTrue(jobs.get("job1").active, "Job1 should start active");
        jobs.get("job1").active = false;
        assertFalse(jobs.get("job1").active, "Job1 should be deactivated");
    }

    @Test
    void testNonExistingJob() {
        assertNull(jobs.get("nonjob"), "Non-job should not exist");
    }
}