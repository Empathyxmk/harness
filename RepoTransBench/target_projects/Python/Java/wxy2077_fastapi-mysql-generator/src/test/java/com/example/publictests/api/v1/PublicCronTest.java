package com.example.publictests.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicCronTest {
    static class Job {
        String id;
        Job(String i) { id=i; }
    }
    static Map<String, Job> jobs = new HashMap<>();

    @BeforeEach
    void setup() {
        jobs.clear();
        jobs.put("pub1", new Job("pub1"));
    }

    @Test
    void testCreatePublicJob() {
        String id = "pub2";
        jobs.put(id, new Job(id));
        assertTrue(jobs.containsKey(id), "Should create and find pub2 job");
    }

    @Test
    void testRemoveJob() {
        jobs.remove("pub1");
        assertFalse(jobs.containsKey("pub1"), "pub1 should no longer exist");
    }
}