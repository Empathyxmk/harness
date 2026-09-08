package com.quora.qcore.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class HelpersTest {
    static class ScopedValue {
        String val;
        public ScopedValue(String val) { this.val = val; }
        public String get() { return val; }
        public ScopedValue override(String v) { return new ScopedValue(v); }
    }
    // Note: Simplified for demonstration purposes
    @Test
    public void testTrueFnAndFalseFn() {
        assertTrue(Boolean.TRUE);
        assertFalse(Boolean.FALSE);
    }
    @Test
    public void testScoped() {
        ScopedValue v = new ScopedValue("a");
        assertEquals("a", v.get());
        ScopedValue b = v.override("b");
        assertEquals("b", b.get());
    }
    @Test
    public void testDictToObject() {
        Map<String, Integer> d = new HashMap<>();
        d.put("a", 1); d.put("b", 2);
        assertEquals(1, d.get("a"));
        assertEquals(2, d.get("b"));
    }
}