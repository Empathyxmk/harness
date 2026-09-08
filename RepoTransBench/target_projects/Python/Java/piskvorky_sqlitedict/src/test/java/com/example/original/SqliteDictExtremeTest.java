package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictExtremeTest {

    @Test
    void testUnicodeKeyAndValue() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            dict.set("ключ", "значение");
            assertEquals("значение", dict.get("ключ"));
        }
    }

    @Test
    void testBinaryLikeValues() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            String binaryData = "\u0000abc\u0000";
            dict.set("bin", binaryData);
            assertEquals(binaryData, dict.get("bin"));
        }
    }
}