package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.core.type.TypeReference;

public class TestPublicJsonTool {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private Object expand(Object obj) {
        if (obj instanceof Map) {
            Map<?,?> map = (Map<?,?>) obj;
            Map<String,Object> out = new LinkedHashMap<>();
            for (Map.Entry<?,?> e : map.entrySet()) {
                if (e.getValue() instanceof Map) {
                    Map<?,?> child = (Map<?,?>) e.getValue();
                    for (Map.Entry<?,?> ce : child.entrySet()) {
                        out.put(e.getKey()+"."+ce.getKey(), ce.getValue());
                    }
                } else {
                    out.put(e.getKey().toString(), e.getValue());
                }
            }
            return out;
        }
        if (obj instanceof List) {
            Map<String,Object> out = new LinkedHashMap<>();
            List<?> l = (List<?>) obj;
            for (int i = 0; i < l.size(); i++) {
                out.put(String.valueOf(i), l.get(i));
            }
            return out;
        }
        return obj;
    }

    private Object restore(Object obj) {
        if (obj instanceof Map) {
            Map<?,?> map = (Map<?,?>) obj;
            boolean numericAll = true;
            for (Object k : map.keySet()) {
                if (!k.toString().matches("\\d+")) numericAll = false;
            }
            if (numericAll) {
                List<Object> l = new ArrayList<>();
                int max = map.size();
                for (int i = 0; i < max; i++)
                    l.add(map.get(String.valueOf(i)));
                return l;
            } else {
                Map<String,Object> out = new LinkedHashMap<>();
                for (Object k : map.keySet()) {
                    String kstr = k.toString();
                    if (kstr.contains(".")) {
                        String[] parts = kstr.split("\\.", 2);
                        if (!out.containsKey(parts[0]))
                            out.put(parts[0], new LinkedHashMap<>());
                        ((Map<String,Object>)out.get(parts[0])).put(parts[1], map.get(k));
                    } else {
                        out.put(kstr, map.get(k));
                    }
                }
                return out;
            }
        }
        return obj;
    }

    @Test
    public void test_public_string() {
        String s = "sss";
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(s, _s);
    }

    @Test
    public void test_public_list() {
        List<Object> s = Arrays.asList("sss", "ttt", 1, 2, Arrays.asList("3"));
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(s, _s);
    }

    @Test
    public void test_public_dict() {
        Map<String,Object> s = new LinkedHashMap<>();
        s.put("s", 1);
        s.put("w", 5);
        Map<String,Object> t = new LinkedHashMap<>();
        t.put("m", 0);
        Map<String,Object> x = new LinkedHashMap<>();
        x.put("y", "z");
        t.put("x", x);
        s.put("t", t);
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(s, _s);
    }

    @Test
    public void test_public_complex() {
        List<Object> s = new ArrayList<>();
        Map<String,Object> a = new LinkedHashMap<>(); a.put("s", 0); s.add(a);
        Map<String,Object> b = new LinkedHashMap<>(); b.put("t", Arrays.asList("2", Collections.singletonMap("x", "z"))); s.add(b);
        s.add(0);
        s.add("w");
        s.add(Arrays.asList("x", "g", 1));
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(((Map<?,?>)s.get(0)), ((Map<?,?>)((List<?>)_s).get(0)));
        assertEquals(((Map<?,?>)s.get(1)), ((Map<?,?>)((List<?>)_s).get(1)));
        assertEquals(s.get(2), ((List<?>)_s).get(2));
        assertEquals(s.get(3), ((List<?>)_s).get(3));
        assertEquals(s.get(4), ((List<?>)_s).get(4));
    }
}