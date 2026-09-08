package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class UtilTest {

    @Test
    public void testFlattenDictSimple() {
        Map<String, Object> dic = new HashMap<>();
        dic.put("a", 1);
        dic.put("b", 2);
        Map<String, Object> flattened = flattenDict(dic);
        assertEquals(2, flattened.size());
        assertEquals(1, flattened.get("a"));
        assertEquals(2, flattened.get("b"));
    }

    @Test
    public void testFlattenDictNested() {
        Map<String, Object> dic = new HashMap<>();
        Map<String, Object> inner = new HashMap<>();
        inner.put("x", 10);
        inner.put("y", 11);
        dic.put("outer", inner);
        dic.put("b", 42);
        Map<String, Object> flat = flattenDict(dic);
        assertEquals(3, flat.size());
        assertEquals(42, flat.get("b"));
        assertEquals(10, flat.get("outer.x"));
        assertEquals(11, flat.get("outer.y"));
    }

    @Test
    public void testFlattenDictList() {
        Map<String, Object> dic = new HashMap<>();
        List<Object> lst = Arrays.asList(1, 2, new HashMap<String, Object>(){{ put("foo", 5); }});
        dic.put("seq", lst);
        Map<String, Object> flat = flattenDict(dic);
        assertEquals(3, flat.size());
        assertEquals(1, flat.get("seq[0]"));
        assertEquals(2, flat.get("seq[1]"));
        assertEquals(5, flat.get("seq[2].foo"));
    }

    public static Map<String, Object> flattenDict(Map<String, Object> dic) {
        Map<String, Object> flat = new HashMap<>();
        flattenImpl("", dic, flat);
        return flat;
    }
    private static void flattenImpl(String prefix, Object obj, Map<String, Object> flat) {
        if (obj instanceof Map) {
            Map<?, ?> m = (Map<?, ?>) obj;
            for (Map.Entry<?,?> entry : m.entrySet()) {
                String key = entry.getKey().toString();
                flattenImpl(prefix.isEmpty() ? key : prefix + "." + key, entry.getValue(), flat);
            }
        } else if (obj instanceof List) {
            List<?> l = (List<?>) obj;
            for (int i=0; i<l.size(); ++i) {
                flattenImpl(prefix + "["+i+"]", l.get(i), flat);
            }
        } else {
            flat.put(prefix, obj);
        }
    }
}