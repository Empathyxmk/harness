package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AutocommitTest {

    @Test
    void testAutocommitSetTrue() {
        SqliteDict dict = new SqliteDict(":memory:", true);
        dict.set("foo", "bar");
        dict.commit(); // should have no effect except not failing
        assertEquals("bar", dict.get("foo"));
        dict.close();
    }

    @Test
    void testAutocommitSetFalseCommitRequired() {
        SqliteDict dict = new SqliteDict(":memory:", false);
        dict.set("foo", "bar");
        assertEquals("bar", dict.get("foo"));
        dict.commit();
        dict.close();
    }

    @Test
    void testAutocommitDoesNotAffectIsolation() {
        String dbName = "file:autocommit-isolation?mode=memory&cache=shared";
        SqliteDict dict1 = new SqliteDict(dbName, true);
        dict1.set("foo", "value");
        dict1.commit();
        dict1.close();

        SqliteDict dict2 = new SqliteDict(dbName, false);
        assertEquals("value", dict2.get("foo"));
        dict2.close();
    }

}