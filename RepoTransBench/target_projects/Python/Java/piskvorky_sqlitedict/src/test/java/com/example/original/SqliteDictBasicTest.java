package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SqliteDictBasicTest {
    @Test
    void testEmptyDict() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertEquals(0, dict.size());
            assertFalse(dict.containsKey("nope"));
        }
    }

    @Test
    void testNonStringKeysAndValues() {
        // This test assumes SqliteDict handles non-string with toString()
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("num", 1234);
            dict.set(42, "meaning");
            assertEquals("1234", dict.get("num"));
            assertEquals("meaning", dict.get(42));
        }
    }

    @Test
    void testIteration() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("a", "b");
            dict.set("x", "y");

            java.util.Set<String> keys = new java.util.HashSet<>(dict.keys());
            assertTrue(keys.contains("a"));
            assertTrue(keys.contains("x"));

            java.util.Collection<String> values = dict.values();
            assertTrue(values.contains("b"));
            assertTrue(values.contains("y"));
        }
    }
}