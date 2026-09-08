package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictErrorsTest {

    @Test
    void testGetMissingKey() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertNull(dict.get("missing"));
        }
    }

    @Test
    void testRemoveMissingKey() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertThrows(Exception.class, () -> {
                dict.remove("notthere");
            });
        }
    }

    @Test
    void testCloseMultipleTimes() {
        SqliteDict dict = new SqliteDict(":memory:", false);
        dict.close();
        dict.close(); // Should be a no-op, not throw
    }

    @Test
    void testIllegalOpen() {
        assertThrows(Exception.class, () -> new SqliteDict("///invalid", false));
    }
}