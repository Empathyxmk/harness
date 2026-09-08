package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class SerializersTest {
    static class DemoSerializer {
        Map<String, Object> data;
        DemoSerializer(Map<String, Object> d) { this.data = d; }
        String getString(String field) { return (String) data.get(field); }
        Integer getInt(String field) { return (Integer) data.get(field); }
    }

    @Test
    void testStringFieldSerialization() {
        Map<String, Object> source = Map.of("foo", "bar");
        DemoSerializer s = new DemoSerializer(source);
        assertEquals("bar", s.getString("foo"));
    }

    @Test
    void testIntFieldSerialization() {
        Map<String, Object> source = Map.of("num", 123);
        DemoSerializer s = new DemoSerializer(source);
        assertEquals(123, s.getInt("num"));
    }

    @Test
    void testMissingFieldSerialization() {
        Map<String, Object> source = Map.of("foo", "bar");
        DemoSerializer s = new DemoSerializer(source);
        assertNull(s.getString("baz"));
    }
}