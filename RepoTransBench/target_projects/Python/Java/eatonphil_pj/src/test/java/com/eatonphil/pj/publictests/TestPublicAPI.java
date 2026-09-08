package com.eatonphil.pj.publictests;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.Pj;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPublicAPI {
    @Test
    public void testFromStringWithDifferentWhitespace() {
        Map<String, Object> result1 = Pj.fromString("{\"foo\":1}");
        Map<String, Object> result2 = Pj.fromString("{\"foo\" : 1}");
        Map<String, Object> result3 = Pj.fromString("{ \"foo\": 1 }");

        assertEquals(result1, result2);
        assertEquals(result1, result3);
        assertEquals(1, result1.get("foo"));

        // Trailing/leading whitespace should be ignored
        Map<String, Object> result4 = Pj.fromString("   {\"foo\":1}   ");
        assertEquals(result1, result4);
    }

    @Test
    public void testToStringSimpleDict() {
        Map<String, Object> m = new HashMap<>();
        m.put("foo", "bar");
        String s = Pj.toString(m);

        assertTrue(s.startsWith("{") && s.endsWith("}"));
        assertTrue(s.contains("\"foo\": \"bar\""));
    }
}