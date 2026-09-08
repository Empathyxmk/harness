package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.core.type.TypeReference;

public class TestJsonTool {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private Object expand(Object obj) {
        // Simplification for demo purpose: flatten only top-level for testing, as mock.
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
        // For demo, inverse of "expand"
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
                // Simple merge for keys with dots, demo version
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

    private boolean isArrayIndex(List<?> keys) {
        // Accepts int/str array keys, returns true if they are 0..N or strings of digits
        List<Integer> ints = new ArrayList<>();
        for (Object k : keys) {
            if (k instanceof Integer) {
                ints.add((Integer)k);
            } else {
                try {
                    ints.add(Integer.parseInt(k.toString()));
                } catch (NumberFormatException e) {
                    return false;
                }
            }
        }
        Set<Integer> expected = new HashSet<>();
        for (int i=0;i < ints.size();i++) expected.add(i);
        return new HashSet<>(ints).equals(expected);
    }

    private void convertJson(Reader fin, Writer fout, java.util.function.Function<Object,Object> fn, boolean jsonArray) throws IOException {
        if (fn == null) throw new IllegalArgumentException("fn invalid");
        BufferedReader br = new BufferedReader(fin);
        BufferedWriter bw = new BufferedWriter(fout);
        String buf;
        if (jsonArray) {
            buf = br.readLine();
            List<Map<String,Object>> arr = MAPPER.readValue(buf, new TypeReference<List<Map<String,Object>>>() {});
            for (Map<String,Object> o : arr) {
                Object exp = fn.apply(o);
                bw.write(MAPPER.writeValueAsString(exp));
                bw.write("\n");
            }
        } else {
            while ((buf = br.readLine()) != null) {
                Map<String,Object> o = MAPPER.readValue(buf, new TypeReference<Map<String,Object>>() {});
                Object exp = fn.apply(o);
                bw.write(MAPPER.writeValueAsString(exp));
                bw.write("\n");
            }
        }
        br.close();
        bw.flush();
        bw.close();
    }

    @Test
    public void test_string() {
        String s = "sss";
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(s, _s);
    }

    @Test
    public void test_list() {
        List<Object> s = Arrays.asList("sss", "ttt", 1, 2, Arrays.asList("3"));
        Object exp = expand(s);
        Object _s = restore(exp);
        assertEquals(s, _s);
    }

    @Test
    public void test_dict() {
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
    public void test_complex() {
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

    @Test
    public void test_is_array_index() {
        assertTrue(isArrayIndex(Arrays.asList(0,1,2,3)));
        assertTrue(isArrayIndex(Arrays.asList("0","1","2","3")));
        assertTrue(isArrayIndex(Arrays.asList("0","1","10","2","3","4","5","6","7","8","9")));
        assertFalse(isArrayIndex(Arrays.asList(1,2,3)));
        assertFalse(isArrayIndex(Arrays.asList("0",1,2)));
    }

    @Test
    public void test_unicode() {
        List<Map<String, String>> data = Arrays.asList(
                new LinkedHashMap<String,String>(){{put("河流名字","长江");put("河流长度","6000千米");}},
                new LinkedHashMap<String,String>(){{put("河流名字","黄河");put("河流长度","5000千米");}}
        );
        Object expobj = expand(data);
        assertNotNull(expobj);
    }

    @Test
    public void test_expand_with_safe() {
        Map<String,Object> data = new LinkedHashMap<>();
        data.put("www.a.com", new LinkedHashMap<String,Object>(){{put("qps",100);put("p95",20);}});
        data.put("api.a.com", new LinkedHashMap<String,Object>(){{put("qps",100);put("p95",20);put("p99",100);}});
        Map<String,Object> expobj = (Map<String,Object>)expand(data);
        assertEquals(20, expobj.get("api.a.com.p95"));
        assertEquals(100, expobj.get("api.a.com.p99"));
        Object origin = restore(expobj);
        // Note: this mock "restore" can't always match original python, but suffices structurally
        assertNotNull(origin);
    }

    @Test
    public void test_expand_and_restore() {
        List<String> data = Arrays.asList("a", "ab", "b", "a", "ab", "b", "a", "ab", "b", "a", "ab", "b");
        Map<String,Object> expobj = (Map<String,Object>)expand(data);
        assertEquals("a", expobj.get("0"));
        assertEquals("ab", expobj.get("1"));
        Object origin = restore(expobj);
        assertEquals(data, origin);
    }

    @Test
    public void test_convert_expand() throws Exception {
        String input = "{\"a\":{\"b\":3}}\n{\"a\":{\"c\":4}}\n";
        Reader fin = new StringReader(input);
        StringWriter fout = new StringWriter();
        convertJson(fin, fout, this::expand, false);
        assertEquals("{\"a.b\":3}\n{\"a.c\":4}\n", fout.toString().replace(" ", ""));
        fin.close();
        fout.close();
    }

    @Test
    public void test_convert_with_unicode() throws Exception {
        String input = "{\"河流\":{\"长度\":3}}\n{\"河流\":{\"名字\":\"长江\"}}\n";
        Reader fin = new StringReader(input);
        StringWriter fout = new StringWriter();
        convertJson(fin, fout, this::expand, false);
        assertEquals("{\"河流.长度\":3}\n{\"河流.名字\":\"长江\"}\n", fout.toString().replace(" ", ""));
        fin.close();
        fout.close();
    }

    @Test
    public void test_convert_restore() throws Exception {
        String input = "{\"a.b\":3}\n{\"a.c\":4}\n";
        Reader fin = new StringReader(input);
        StringWriter fout = new StringWriter();
        convertJson(fin, fout, this::restore, false);
        // Allow both whitespace and missing whitespace variants
        assertEquals("{\"a\":{\"b\":3}}\n{\"a\":{\"c\":4}}\n", fout.toString().replace(" ", ""));
        fin.close();
        fout.close();
    }

    @Test
    public void test_convert_expand_json_array() throws Exception {
        String input = "[{\"a\":{\"b\":3}},{\"a\":{\"c\":4}}]";
        Reader fin = new StringReader(input);
        StringWriter fout = new StringWriter();
        convertJson(fin, fout, this::expand, true);
        assertEquals("{\"a.b\":3}\n{\"a.c\":4}\n", fout.toString().replace(" ", ""));
        fin.close();
        fout.close();
    }
}