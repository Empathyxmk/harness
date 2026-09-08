package com.example.original;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SqliteDictExtremesTest {

    @Test
    void testVeryLargeValue() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 1024 * 1024; i++) sb.append('A');
            String huge = sb.toString();
            dict.set("huge", huge);
            assertEquals(huge, dict.get("huge"));
        }
    }

    @Test
    void testHighUnicode() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            String emoji = "😀😃😄😁";
            dict.set("emoji", emoji);
            assertEquals(emoji, dict.get("emoji"));
        }
    }
}