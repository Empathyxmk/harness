package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TempSqliteDictTest {
    @Test
    void testTempDbBehavior() {
        // Use :memory: so nothing persisted between runs
        SqliteDict dict = new SqliteDict(":memory:", false);
        dict.set("a", "temp-val");
        assertEquals("temp-val", dict.get("a"));
        dict.close();
        SqliteDict dict2 = new SqliteDict(":memory:", false);
        assertNull(dict2.get("a"));
        dict2.close();
    }

    @Test
    void testMultipleTempDbInstancesAreIndependent() {
        SqliteDict dict1 = new SqliteDict(":memory:", false);
        SqliteDict dict2 = new SqliteDict(":memory:", false);
        dict1.set("foo", "1");
        dict2.set("bar", "2");
        assertEquals("1", dict1.get("foo"));
        assertNull(dict1.get("bar"));
        assertEquals("2", dict2.get("bar"));
        assertNull(dict2.get("foo"));
        dict1.close();
        dict2.close();
    }
}