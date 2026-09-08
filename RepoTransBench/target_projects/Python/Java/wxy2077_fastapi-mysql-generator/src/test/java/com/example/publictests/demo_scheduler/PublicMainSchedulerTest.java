package com.example.publictests.demo_scheduler;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDateTime;
import java.util.*;

class PublicMainSchedulerTest {

    public static List<LocalDateTime> nextTimes(LocalDateTime base, long minutesDelta, int cnt) {
        List<LocalDateTime> times = new ArrayList<>();
        LocalDateTime t = base;
        for (int i = 0; i < cnt; i++) {
            t = t.plusMinutes(minutesDelta);
            times.add(t);
        }
        return times;
    }

    @Test
    void testPublicSchedule() {
        LocalDateTime base = LocalDateTime.of(2024, 1, 2, 8, 0);
        List<LocalDateTime> out = nextTimes(base, 30, 2);
        assertEquals(2, out.size());
        assertTrue(out.get(0).isAfter(base));
        assertEquals(30, java.time.Duration.between(base, out.get(0)).toMinutes());
    }
}