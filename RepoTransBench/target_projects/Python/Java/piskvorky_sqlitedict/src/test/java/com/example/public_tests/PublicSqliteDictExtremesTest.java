package com.example.public_tests;

import com.example.SqliteDict;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSqliteDictExtremesTest {

    @Test
    void testLargeValueAndKey() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 10_000; i++) sb.append("k");
            String hugeKey = sb.toString();
            String hugeVal = sb.reverse().toString();
            dict.set(hugeKey, hugeVal);
            assertEquals(hugeVal, dict.get(hugeKey));
        }
    }

    @Test
    void testSpecialCharsAndUnicode() {
        try (SqliteDict dict = new SqliteDict(":memory:", false)) {
            String special = "!@#$%^&*()_+-=[]{}|;':,.<>/?";
            String uni = "你好, мир, hello";
            dict.set("special", special);
            dict.set("uni", uni);
            assertEquals(special, dict.get("special"));
            assertEquals(uni, dict.get("uni"));
        }
    }

}