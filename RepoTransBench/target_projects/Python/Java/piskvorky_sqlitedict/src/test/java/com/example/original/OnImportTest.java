package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OnImportTest {

    @Test
    void testBasicOnImport() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertNotNull(dict);
        }
    }

    @Test
    void testOnImportCreateAndRead() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("k", "v");
        }
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            assertNull(dict.get("k"));  // new memory DB, should not persist
        }
    }

}