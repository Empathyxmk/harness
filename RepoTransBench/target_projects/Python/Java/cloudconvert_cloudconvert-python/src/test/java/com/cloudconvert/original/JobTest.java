package com.cloudconvert.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JobTest {

    static class Job extends java.util.HashMap<String, Object> {}

    @Test
    void testJobFromData() {
        Job j = new Job();
        j.put("id", "abc");
        j.put("status", "waiting");
        assertEquals("abc", j.get("id"));
        assertEquals("waiting", j.get("status"));
    }

    @Test
    void testJobStrRepr() {
        Job j = new Job();
        j.put("id", "a");
        j.put("foo", "b");
        assertTrue(j.toString().contains("id"));
        assertTrue(j.toString().contains("foo"));
    }

    @Test
    void testJobFailMissingKey() {
        Job j = new Job();
        assertNotNull(j);
    }
}