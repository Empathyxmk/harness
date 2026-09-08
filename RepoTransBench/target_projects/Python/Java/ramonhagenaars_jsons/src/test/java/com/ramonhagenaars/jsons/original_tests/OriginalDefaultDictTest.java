package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.util.HashMap;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultDictTest {

    @Test
    void testDictInsertAndGet() {
        HashMap<String, Integer> dict = new HashMap<>();
        dict.put("key1", 99);
        dict.put("abc", -88);
        assertEquals(99, dict.get("key1").intValue());
        assertEquals(-88, dict.get("abc").intValue());
    }

    @Test
    void testDictPutOverride() {
        HashMap<String, String> dict = new HashMap<>();
        dict.put("a", "one");
        dict.put("a", "two");
        assertEquals("two", dict.get("a"));
    }
}