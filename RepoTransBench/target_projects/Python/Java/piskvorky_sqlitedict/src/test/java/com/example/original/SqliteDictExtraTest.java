package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictExtraTest {

    @Test
    void testClearAndReopen() {
        String dbName = "file:extra-test-reopen?mode=memory&cache=shared";
        try (SqliteDict dict = new SqliteDict(dbName, false)) {
            dict.set("foo", "bar");
            dict.clear();
            assertEquals(0, dict.size());
        }
        try (SqliteDict dict = new SqliteDict(dbName, false)) {
            assertEquals(0, dict.size());
        }
    }

    @Test
    void testKeysSet() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("a", "b");
            dict.set("c", "d");
            Set<String> keys = new java.util.HashSet<>(dict.keys());
            assertEquals(2, keys.size());
            assertTrue(keys.contains("a"));
            assertTrue(keys.contains("c"));
        }
    }

    @Test
    void testOverwriteValue() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("dup", "first");
            dict.set("dup", "second");
            assertEquals("second", dict.get("dup"));
        }
    }
}