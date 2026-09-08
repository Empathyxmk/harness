package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictCoverageExtTest {

    @Test
    void testUpdateAndPutAll() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("one", "1");
            dict.set("two", "2");
            dict.update("one", "uno"); // Assume update replaces value
            assertEquals("uno", dict.get("one"));

            java.util.Map<String, String> batch = new java.util.HashMap<>();
            batch.put("three", "3");
            batch.put("four", "4");
            dict.putAll(batch);
            assertEquals("3", dict.get("three"));
            assertEquals("4", dict.get("four"));
        }
    }

    @Test
    void testBatchRemove() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("x", "1");
            dict.set("y", "2");
            dict.set("z", "3");

            assertTrue(dict.containsKey("x"));
            assertTrue(dict.containsKey("y"));

            dict.batchRemove(new String[]{"x", "z"});
            assertFalse(dict.containsKey("x"));
            assertFalse(dict.containsKey("z"));
            assertTrue(dict.containsKey("y"));
        }
    }

    @Test
    void testProtectionAgainstMultipleCommit() {
        SqliteDict dict = new SqliteDict(":memory:", false);
        dict.commit();
        dict.commit();
        dict.close();
        // Should not throw errors
    }

    @Test
    void testReadonlyMode() {
        String dbName = "file:coverage-ext-readonly?mode=memory&cache=shared";
        SqliteDict dict = new SqliteDict(dbName, false);
        dict.set("a", "A");
        dict.close();

        SqliteDict readOnly = new SqliteDict(dbName, false);
        assertEquals("A", readOnly.get("a"));
        readOnly.close();
    }
}