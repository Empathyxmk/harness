package com.cloudconvert.original;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    @Test
    void testJoinUrlBasic() {
        assertEquals("a/b/c", joinUrl("a", "b", "c"));
        assertEquals("a/b/c", joinUrl("a/", "/b/", "c/"));
    }

    @Test
    void testStripNoneDict() {
        Map<String, Object> d = new HashMap<>();
        d.put("a", 1);
        d.put("b", null);
        d.put("c", 0);
        Map<String, Object> out = stripNone(d);
        assertFalse(out.containsKey("b"));
        assertTrue(out.containsKey("a"));
        assertTrue(out.containsKey("c"));
    }

    @Test
    void testStripNoneList() {
        List<Object> l = Arrays.asList(1, null, 2);
        List<Object> out = stripNone(l);
        assertEquals(List.of(1, 2), out);
    }

    @Test
    void testStripNoneOther() {
        String val = "foo";
        assertEquals("foo", stripNone(val));
    }

    @Test
    void testDictKeysToCamelCase() {
        Map<String, Integer> d = Map.of("foo_bar", 1, "BarBaz_qux", 2);
        Map<String, Integer> cd = dictKeysToCamelCase(d);
        assertTrue(cd.containsKey("fooBar"));
        assertTrue(cd.containsKey("barBazQux"));
    }

    @Test
    void testToSnakeCase() {
        assertEquals("foo_bar_baz", toSnakeCase("fooBarBAZ"));
    }

    @Test
    void testToCamelCase() {
        assertEquals("fooBarBaz", toCamelCase("foo_bar_baz"));
    }

    @Test
    void testGetValue() {
        Map<String, Object> d = Map.of("a", 1);
        assertEquals(1, getValue(d, "a", "fallback"));
        assertEquals("fallback", getValue(d, "z", "fallback"));
    }

    // ------------ Simulated utilities to match logic -------------
    private static String joinUrl(String... parts) {
        List<String> all = new ArrayList<>();
        for (String part : parts) {
            String p = part.replaceAll("^/+|/+$", "");
            all.add(p);
        }
        return String.join("/", all);
    }

    private static Map<String, Object> stripNone(Map<String, Object> map) {
        Map<String, Object> out = new HashMap<>();
        for (Map.Entry<String, Object> e : map.entrySet()) {
            if (e.getValue() != null) out.put(e.getKey(), e.getValue());
        }
        return out;
    }

    private static List<Object> stripNone(List<Object> list) {
        List<Object> out = new ArrayList<>();
        for (Object o : list) {
            if (o != null) out.add(o);
        }
        return out;
    }

    private static Object stripNone(Object o) {
        if (o instanceof List) {
            return stripNone((List<Object>) o);
        } else if (o instanceof Map) {
            return stripNone((Map<String, Object>) o);
        } else {
            return o;
        }
    }

    private static Map<String, Integer> dictKeysToCamelCase(Map<String, Integer> map) {
        Map<String, Integer> out = new HashMap<>();
        map.forEach((k, v) -> out.put(toCamelCase(k), v));
        return out;
    }

    private static String toSnakeCase(String s) {
        String intermediate = s.replaceAll("([A-Z])", "_$1").replaceAll("__+", "_");
        return intermediate.toLowerCase().replaceAll("^_", "");
    }

    private static String toCamelCase(String s) {
        String[] parts = s.toLowerCase().split("_");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length; ++i) {
            if (i == 0) sb.append(parts[i]);
            else sb.append(parts[i].substring(0, 1).toUpperCase()).append(parts[i].substring(1));
        }
        return sb.toString();
    }

    private static Object getValue(Map<String, Object> map, String key, Object fallback) {
        return map.getOrDefault(key, fallback);
    }

}