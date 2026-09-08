package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictEdgecasesTest {

    @Test
    void testNullKeyAndValue() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertThrows(IllegalArgumentException.class, () -> {
                dict.set(null, "value");
            });
            assertThrows(IllegalArgumentException.class, () -> {
                dict.set("key", null);
            });
        }
    }

    @Test
    void testLargeNumberOfKeys() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            for (int i = 0; i < 1000; i++) dict.set("k" + i, "v" + i);
            assertEquals(1000, dict.size());
            for (int i = 0; i < 1000; i++) {
                assertEquals("v" + i, dict.get("k" + i));
            }
        }
    }

    @Test
    void testLongKeys() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            String longKey = "k".repeat(4096);
            dict.set(longKey, "test");
            assertEquals("test", dict.get(longKey));
        }
    }
}