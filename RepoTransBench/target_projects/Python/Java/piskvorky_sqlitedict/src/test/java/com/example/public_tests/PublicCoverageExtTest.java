package com.example.public_tests;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicCoverageExtTest {

    @Test
    void testBatchPut() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            java.util.Map<String, String> batch = new java.util.HashMap<>();
            batch.put("x", "X");
            batch.put("y", "Y");
            dict.putAll(batch);
            assertEquals("X", dict.get("x"));
            assertEquals("Y", dict.get("y"));
        }
    }

    @Test
    void testBatchDelete() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("k1", "v1");
            dict.set("k2", "v2");
            dict.batchRemove(new String[]{"k1", "k3"});
            assertFalse(dict.containsKey("k1"));
            assertTrue(dict.containsKey("k2"));
        }
    }
}