package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictCoreTest {

    @Test
    void testPutGetRemove() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("a", "aaa");
            assertEquals("aaa", dict.get("a"));
            dict.remove("a");
            assertNull(dict.get("a"));
        }
    }

    @Test
    void testPersistence() {
        String dbName = "file:test-persistence?mode=memory&cache=shared";
        try (SqliteDict dict = new SqliteDict(dbName, false)) {
            dict.set("k", "val");
        }
        // Simulate closing and reopening to check persistence for backing database
        try (SqliteDict dict = new SqliteDict(dbName, false)) {
            assertEquals("val", dict.get("k"));
        }
    }

    @Test
    void testContainsKeyAndSize() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertEquals(0, dict.size());
            dict.set("x", "y");
            assertTrue(dict.containsKey("x"));
            assertEquals(1, dict.size());
            dict.remove("x");
            assertFalse(dict.containsKey("x"));
            assertEquals(0, dict.size());
        }
    }

    @Test
    void testClear() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("k1", "v1");
            dict.set("k2", "v2");
            dict.clear();
            assertEquals(0, dict.size());
            assertFalse(dict.containsKey("k1"));
            assertFalse(dict.containsKey("k2"));
        }
    }

    @Test
    void testKeysValuesItems() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("alpha", "a");
            dict.set("beta", "b");
            List<String> keys = dict.keys();
            assertTrue(keys.contains("alpha"));
            assertTrue(keys.contains("beta"));
            List<String> values = dict.values();
            assertTrue(values.contains("a"));
            assertTrue(values.contains("b"));
        }
    }
}