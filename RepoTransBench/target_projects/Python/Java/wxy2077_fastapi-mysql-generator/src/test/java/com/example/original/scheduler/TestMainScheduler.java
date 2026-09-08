package com.example.original.scheduler;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDateTime;
import java.util.*;

class TestMainScheduler {

    static class ScheduledJob {
        String name;
        List<LocalDateTime> times;
        ScheduledJob(String n, List<LocalDateTime> t) { name = n; times = t; }
    }

    static Map<String, ScheduledJob> jobs = new HashMap<>();

    static List<LocalDateTime> computeTimes(LocalDateTime start, long intervalMinutes, int count) {
        List<LocalDateTime> result = new ArrayList<>();
        LocalDateTime curr = start;
        for (int i = 0; i < count; i++) {
            curr = curr.plusMinutes(intervalMinutes);
            result.add(curr);
        }
        return result;
    }

    @BeforeEach
    void setup() {
        jobs.clear();
        jobs.put("jobA", new ScheduledJob("jobA", computeTimes(LocalDateTime.of(2024,1,1,0,0), 60, 3)));
    }

    @Test
    void testComputeTimes() {
        LocalDateTime base = LocalDateTime.of(2024, 1, 2, 8, 0);
        List<LocalDateTime> times = computeTimes(base, 30, 2);
        assertEquals(2, times.size());
        assertTrue(times.get(0).isAfter(base));
        assertEquals(30, java.time.Duration.between(base, times.get(0)).toMinutes());
    }

    @Test
    void testAddScheduledJob() {
        LocalDateTime base = LocalDateTime.now();
        List<LocalDateTime> times = computeTimes(base, 45, 2);
        jobs.put("jobB", new ScheduledJob("jobB", times));
        assertTrue(jobs.containsKey("jobB"));
        assertEquals(2, jobs.get("jobB").times.size());
    }

    @Test
    void testRemoveJob() {
        jobs.remove("jobA");
        assertFalse(jobs.containsKey("jobA"));
    }

    @Test
    void testScheduledTimesLength() {
        assertEquals(3, jobs.get("jobA").times.size());
    }
}