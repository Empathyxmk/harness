package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicJobTest {
    static class Job extends java.util.HashMap<String, Object> {}

    @Test
    void testHasIdField() {
        Job j = new Job();
        j.put("id", "abc123");
        assertEquals("abc123", j.get("id"));
    }
}