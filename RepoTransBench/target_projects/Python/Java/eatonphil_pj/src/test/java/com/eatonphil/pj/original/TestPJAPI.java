package com.eatonphil.pj.original;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.Pj;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPJAPI {
    @Test
    public void testToStringAndFromString() {
        // toString should handle basic Java types and match simple expectations
        Map<String, Object> m = new HashMap<>();
        m.put("foo", 1);
        assertEquals("{\"foo\": 1}", Pj.toString(m));

        m.put("bar", "baz");
        assertEquals("{\"foo\": 1, \"bar\": \"baz\"}", Pj.toString(m));

        m.put("a", true);
        assertEquals("{\"foo\": 1, \"bar\": \"baz\", \"a\": true}", Pj.toString(m));

        List<Object> l = new ArrayList<>();
        l.add(1);
        l.add("two");
        l.add(false);
        assertEquals("[1, \"two\", false]", Pj.toString(l));

        // null mapping
        m.put("n", null);
        assertTrue(Pj.toString(m).contains("\"n\": None"));

        // fromString should gracefully parse simple dict
        Map<String, Object> parsed = Pj.fromString("{\"foo\": 1, \"bar\": 2}");
        // The parser uses HashMap, equals should work for simple key/val
        assertEquals(2, parsed.size());
        assertEquals(1, parsed.get("foo"));
        assertEquals(2, parsed.get("bar"));
    }
}