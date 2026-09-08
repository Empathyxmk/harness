package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NamedSqliteDictTest {

    @Test
    void testOpenNamedDatabase() {
        String dbName = "file:named-db?mode=memory&cache=shared";
        try (SqliteDict dict = new SqliteDict(dbName, false)) {
            dict.set("one", "1");
            dict.set("two", "2");
            assertEquals("1", dict.get("one"));
            assertEquals("2", dict.get("two"));
        }
    }

    @Test
    void testMultipleNamedDbs() {
        String db1 = "file:db-one?mode=memory&cache=shared";
        String db2 = "file:db-two?mode=memory&cache=shared";
        try (SqliteDict d1 = new SqliteDict(db1, false)) {
            d1.set("key", "value1");
        }
        try (SqliteDict d2 = new SqliteDict(db2, false)) {
            d2.set("key", "value2");
        }
        try (SqliteDict d1 = new SqliteDict(db1, false); SqliteDict d2 = new SqliteDict(db2, false)) {
            assertEquals("value1", d1.get("key"));
            assertEquals("value2", d2.get("key"));
        }
    }

}