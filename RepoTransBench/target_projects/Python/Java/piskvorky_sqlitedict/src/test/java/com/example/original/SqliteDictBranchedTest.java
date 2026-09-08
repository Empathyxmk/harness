package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictBranchedTest {

    @Test
    void testBranchingAndRebasing() {
        String dbName = "file:test-branching?mode=memory&cache=shared";
        try (SqliteDict dict1 = new SqliteDict(dbName, false)) {
            dict1.set("x", "1");
        }
        try (SqliteDict dict2 = new SqliteDict(dbName, false)) {
            assertEquals("1", dict2.get("x"));
            dict2.set("y", "2");
        }
        try (SqliteDict dict3 = new SqliteDict(dbName, false)) {
            assertEquals("1", dict3.get("x"));
            assertEquals("2", dict3.get("y"));
        }
    }

    @Test
    void testBranchIsolation() {
        String db1 = "file:test-branch1?mode=memory&cache=shared";
        String db2 = "file:test-branch2?mode=memory&cache=shared";
        try (SqliteDict dict1 = new SqliteDict(db1, false)) {
            dict1.set("a", "1");
        }
        try (SqliteDict dict2 = new SqliteDict(db2, false)) {
            dict2.set("b", "2");
        }
        try (SqliteDict dict1 = new SqliteDict(db1, false)) {
            assertEquals("1", dict1.get("a"));
            assertNull(dict1.get("b"));
        }
        try (SqliteDict dict2 = new SqliteDict(db2, false)) {
            assertEquals("2", dict2.get("b"));
            assertNull(dict2.get("a"));
        }
    }
}